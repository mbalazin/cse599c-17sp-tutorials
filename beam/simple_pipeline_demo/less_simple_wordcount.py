# 5-20-17
# Super simple Beam example of counting words 
# To run: python less-simple-wordcount.py <inputFile> <outputFile>

import logging
logging.getLogger().setLevel(logging.ERROR)
logging.basicConfig()

import re
import sys
import apache_beam as beam
from apache_beam.io import ReadFromText
from apache_beam.io import WriteToText
from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam.options.pipeline_options import StandardOptions

from apache_beam.metrics import Metrics
from apache_beam.metrics.metric import MetricsFilter


class WordExtractingDoFn(beam.DoFn):
  """Parse each line of input text into words."""

  def __init__(self):
    super(WordExtractingDoFn, self).__init__()
    self.word_counter = Metrics.counter(self.__class__, 'num_words')
    self.word_lengths_dist = Metrics.distribution(
        self.__class__, 'word_len_dist')

  def process(self, line):
    """Returns an iterator over the words of this line.

    Args:
      line: the line of text being processed

    Returns:
      The processed line.
    """
    text_line = line.strip()
    words = re.findall(r'[A-Za-z\']+', text_line)
    for w in words:
      self.word_counter.inc()
      self.word_lengths_dist.update(len(w))
    return words


def run(input_file, output_file):
  """Main entry point; defines and runs the wordcount pipeline."""
  
  options = PipelineOptions()
  options.view_as(StandardOptions).runner = 'DirectRunner'

  p = beam.Pipeline(options=options)

  # Read the text file[pattern] into a PCollection.
  lines = p | 'read' >> ReadFromText(input_file)

  # Count the occurrences of each word.
  counts = (lines
            | 'split' >> (beam.ParDo(WordExtractingDoFn())
                          .with_output_types(unicode))
            | 'pair_with_one' >> beam.Map(lambda x: (x, 1))
            | 'group' >> beam.GroupByKey()
            | 'count' >> beam.Map(lambda (word, ones): (word, sum(ones))))

  # Format the counts into a PCollection of strings.
  output = counts | 'format' >> beam.Map(lambda (word, c): '%s: %s' % (word, c))

  # Write the output using a "Write" transform that has side effects.
  # pylint: disable=expression-not-assigned
  output | 'write' >> WriteToText(output_file)

  # Actually run the pipeline (all operations above are deferred).
  result = p.run()
  result.wait_until_finish()

  word_lengths_filter = MetricsFilter().with_name('word_len_dist')
  query_result = result.metrics().query(word_lengths_filter)
  if query_result['distributions']:
    word_lengths_dist = query_result['distributions'][0]
    print 'average word length: %d', word_lengths_dist.committed.mean
  num_words_filer = MetricsFilter().with_name('num_words')
  query_result = result.metrics().query(num_words_filer)
  if query_result['counters']:
    total_words = query_result['counters'][0]
    print 'Number of total words: ' + str(total_words.committed)


if __name__ == '__main__':
  run(sys.argv[1], sys.argv[2])
