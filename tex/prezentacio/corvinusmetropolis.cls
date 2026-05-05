\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{corvinusmetropolis}[2022/04/15 corvinusmetropolis v0.2]
\DeclareOption*{\PassOptionsToClass{\CurrentOption}{beamer}}
\ProcessOptions
\LoadClass{beamer}
%
\RequirePackage{orcidlink}
\synctex=1
%
\ifboolexpr{bool {xetex} or bool {luatex}}{
    \ClassInfo{corvinusmetropolis}{Use all of beamer options.\MessageBreak
    LaTeX package corvinusmetropolis is loaded}
    \RequirePackage{fontspec}%The package fontspec is also loaded by metropolis.sty but I do not need the option no-math.
    }{
    \ifpdf 
        \ClassInfo{corvinusmetropolis}{Wrong tex engine. Usage: lualatex <filename> or xelatex <filename>\MessageBreak
                     pdflatex also works but does not use Corvinus fonts.}
    \else
        \ClassError{corvinusmetropolis}{Wrong tex engine}{Usage: lualatex <filename> or xelatex <filename>\MessageBreak
                     pdflatex also works but does not use Corvinus fonts.}
    \fi
    }
%
\newcommand{\@email}{}
\newcommand{\email}[1]{\renewcommand{\@email}{#1}}
\newcommand{\putemail}{\url{\@email}}
%
\usetheme[outer/progressbar=foot, titleformat=smallcaps, subsectionpage=progressbar, block=fill]{metropolis}
\ifboolexpr{bool {xetex} or bool {luatex}}%
    {%
    \iffontsavailable{TT_Nooks_Regular, Calluna_Italic, Calluna_Regular}
        {%
        \setsansfont[BoldFont={TT_Nooks_Regular},ItalicFont={Calluna_Italic}]{Calluna_Regular}%
        \ClassInfo{corvinusmetropolis}{Corvinus recommended fonts TT Nooks and Calluna work properly even if Overleaf is used!}%
        }
        {
        \ClassInfo{corvinusmetropolis}{Assume it is not Overleaf! Turning to  system fonts.}%
        \iffontsavailable{TT Nooks, Calluna}
            {%
            \setsansfont[BoldFont={TT Nooks-Regular},ItalicFont={Calluna-It}]{Calluna-Regular}%
            \ClassInfo{corvinusmetropolis}{Corvinus recommended fonts TT Nooks and Calluna work properly!}%
            }
            {\ClassInfo{corvinusmetropolis}{At least one of Corvinus recommended fonts is missing. \MessageBreak
            Upload the fonts TT Nooks and Calluna to Overleaf, or install these fonts locally!}
            }
        }
    }%
    {
        \ClassInfo{corvinusmetropolis}{You need to compile XeLaTeX os LuaLatex to use the Corvinus recommended fonts TT Nooks and Calluna}
    }
%

% other official color variations:
% primary: Old original: 1B213E, Light red: FFDEDE, Red: FF4132, Dark red: 410500, Light green: E1FFD9, Green: 0ACD5A, Dark green: 002300
% secondry: Old original: 855C24, Light purple: E3DEFF, Purple: A07DF5, Dark purple: 2D004B, Light blue: CDF0FF, Blue: 32B4E6, Dark blue: 002332

% original color scheme
% \definecolor{SecondaryColor}{HTML}{855C24}
% \definecolor{PrimaryColor}{HTML}{1B213E}

% updated purple color scheme
% \definecolor{SecondaryColor}{HTML}{32B4E6}
% \definecolor{PrimaryColor}{HTML}{2D004B}

% red-brown color scheme
\definecolor{SecondaryColor}{HTML}{FF4132}
\definecolor{PrimaryColor}{HTML}{410500}

\setbeamercolor{normal text}{fg=PrimaryColor}
\setbeamercolor{alerted text}{fg=SecondaryColor, bg=PrimaryColor}

\setbeamertemplate{blocks}[rounded]
%
\newcommand{\thankyoupage}[1]{
    \frametitle{#1}
    \includegraphics[width=.5\textwidth]{./corvinus-logos/color_notext.pdf}
    % \includegraphics[width=.25\textwidth]{./corvinus-logos/black_notext.pdf}
    \hfill{\putemail}
}
\newcommand{\closingframes}[1]{
    \metroset{outer/numbering=none}
    \frame{\thankyoupage{#1}}
}
\newcommand{\openingframes}[1]{
    \metroset{outer/numbering=none, outer/progressbar=foot}
    \frame{\titlepage}
    % \frame{\frametitle{#1}\tableofcontents}
    \metroset{outer/numbering=counter, outer/progressbar=foot, block=transparent}%
}
\newcommand{\myinstlogo}{./corvinus-logos/color_simple_HUN.pdf}

\endinput
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
For Overleaf users!
Upload the Corvinus recommended fonts to Overleaf and Overleaf manages the font installation.
The required font files are as follows:

Calluna_Bold_Italic.otf
Calluna_Bold.otf
Calluna_Heavy.otf
Calluna_Italic.otf
Calluna_Light.otf
Calluna_Regular.otf
Calluna_Semi_Bold_Italic.otf
Calluna_Semi_Bold.otf
TT_Nooks_Bold.otf
TT_Nooks_Heavy.otf
TT_Nooks_Light.otf
TT_Nooks_Regular.otf

If you need these files send an email to me, I share an Overleaf link where you can find corvinusmetropolis installed.
