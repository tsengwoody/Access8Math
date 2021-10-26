from delimiter import LaTeX as LaTeX_delimiter, AsciiMath as AsciiMath_delimiter

translate_dict = {
	ord("$"): r"\$",
	ord("("): r"\(",
	ord(")"): r"\)",
	ord("\\"): r"\\",
}


def delimiterRegularExpression(delimiter):
	latex_restring = r"(?<=[^\\])(?P<ld_start>{delimiter_start})(?P<latex>[^\n]*?[^\\^\n])?(?P<ld_end>{delimiter_end})".format(
		delimiter_start=LaTeX_delimiter[delimiter["latex"]]["start"].translate(translate_dict),
		delimiter_end=LaTeX_delimiter[delimiter["latex"]]["end"].translate(translate_dict),
	)
	latex_restring_start = r"(?P<lsd_start>{delimiter_start})(?P<latex_start>[^\n]*?[^\\^\n])?(?P<lsd_end>{delimiter_end})".format(
		delimiter_start=LaTeX_delimiter[delimiter["latex"]]["start"].translate(translate_dict),
		delimiter_end=LaTeX_delimiter[delimiter["latex"]]["end"].translate(translate_dict),
	)
	asciimath_restring = r"(?<=[^\\])(?P<ad_start>{delimiter_start})(?P<asciimath>[^\n]*?[^\\^\n])?(?P<ad_end>{delimiter_end})".format(
		delimiter_start=AsciiMath_delimiter[delimiter["asciimath"]]["start"].translate(translate_dict),
		delimiter_end=AsciiMath_delimiter[delimiter["asciimath"]]["end"].translate(translate_dict),
	)
	asciimath_restring_start = r"(?P<asd_start>{delimiter_start})(?P<asciimath_start>[^\n]*?[^\\^\n])?(?P<asd_end>{delimiter_end})".format(
		delimiter_start=AsciiMath_delimiter[delimiter["asciimath"]]["start"].translate(translate_dict),
		delimiter_end=AsciiMath_delimiter[delimiter["asciimath"]]["end"].translate(translate_dict),
	)

	return {
		"asciimath": asciimath_restring,
		"asciimath_start": asciimath_restring_start,
		"latex": latex_restring,
		"latex_start": latex_restring_start,
		"mathml": r"(?P<mathml><math.*?>.*?</math.*?>)"
	}


latex_bracket_dollar = {
	"latex_dollar": r"(?<=[^\\])(?P<ld_start_dollar>\$)(?P<latex>[^\n]*?[^\\^\n])?(?P<ld_end_dollar>\$)",
	"latex_start_dollar": r"(?P<lsd_start_dollar>\$)(?P<latex_start>[^\n]*?[^\\^\n])?(?P<lsd_end_dollar>\$)",
	"latex_bracket": r"(?<=[^\\])(?P<ld_start_bracket>\\\()(?P<latex>[^\n]*?[^\\^\n])?(?P<ld_end_bracket>\\\))",
	"latex_start_bracket": r"(?P<lsd_start_bracket>\\\()(?P<latex_start>[^\n]*?[^\\^\n])?(?P<lsd_end_bracket>\\\))",
}
