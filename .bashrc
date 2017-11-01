alias lapa="ssh -Y thartland@lapa.lancs.ac.uk"

alias format-style="clang-format -i -style=\"{BasedOnStyle: llvm, IndentWidth: 4, ColumnLimit: 140}\""

function file_from_lapa() {
	scp thartland@lapa.lancs.ac.uk:/home/atlas/thartland/"$1" .
}
