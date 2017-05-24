# 5-20-17
# Super simple Beam example of counting words 
# To run: python super-simple-wordcount.py <inputFile> <outputFile>

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

def process_line(line):
  """Returns an iterator over the words of this line.

  Args:
    line: the line being processed

  Returns:
    The processed line.
  """
  text_line = line.strip()
  words = re.findall(r'[A-Za-z\']+', text_line)
  return words


def run(input_file, output_file):
  """Main entry point; defines and runs the wordcount pipeline."""

  options = PipelineOptions()
  options.view_as(StandardOptions).runner = 'DirectRunner'

  p = beam.Pipeline(options=options)

  # Read the text file into a PCollection.
  # Note: the process names can be whatever you want; 
  #       they just label the steps (e.g., when you're examining the pipeline on the google cloud platform)

  lines = p | 'read' >> ReadFromText(input_file)

  # Count the occurrences of each word.
  counts = (lines
            | 'split' >> beam.ParDo(process_line)
                          .with_output_types(unicode)
            | 'pair_with_one' >> beam.Map(lambda x: (x, 1))
            | 'group' >> beam.GroupByKey()
            | 'count' >> beam.Map(lambda (word, ones): (word, sum(ones))))

  # Format the counts into a PCollection of strings.
  output = counts | 'format' >> beam.Map(lambda (word, c): '%s: %s' % (word, c))

  # Write the output using a "Write" transform that has side effects.
  output | 'write' >> WriteToText(output_file)

  # Actually run the pipeline (all operations above are deferred).
  result = p.run()
  result.wait_until_finish()


if __name__ == '__main__':
  run(sys.argv[1], sys.argv[2])
