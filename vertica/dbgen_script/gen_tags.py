tagstr="android api art ask assembly audio compsci crypto cryptocurrencies distributed dotnet elixir devops linux graphics hardware hasekll lisp lua mac math perl person philosophy php programming scala scaling science secure unix vcs video vim virtualization practices privacy python visualization show web slides rant reversing networking ml ios javascript event finance c databases browsers erlang emacs meta cogsci debugging games compilers freebsd job ruby windows swift rust openbsd design go pdf satire testing"

tags = tagstr.split(" ")
i = 1
for t in tags:
	i += 1
	print ",".join([str(i), t])
