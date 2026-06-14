\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{corvinusmetropolis}[2022/04/15 corvinusmetropolis v0.2]
\DeclareOption*{\PassOptionsToClass{\CurrentOption}{beamer}}
\ProcessOptions
\LoadClass{beamer}
%
\RequirePackage{orcidlink, fontspec}
\RequirePackage[T1]{fontenc}
\RequirePackage[style=apa, backend=biber]{biblatex}
\RequirePackage{csquotes}
%
\synctex=1
%
%
\newcommand{\@email}{}
\newcommand{\email}[1]{\renewcommand{\@email}{#1}}
\newcommand{\putemail}{\texttt{\href{mailto:\@email}{\@email}}}
\newcommand{\imp}[1]{\alert{\textit{#1}}}
%
\usetheme[outer/progressbar=foot, titleformat=smallcaps, subsectionpage=progressbar, block=fill]{metropolis}
\usefonttheme{professionalfonts}
%
\setmainfont[UprightFont = {./fonts/Calluna-Regular.otf}, ItalicFont  = {./fonts/Calluna-Italic.otf}, BoldFont    = {./fonts/TT-Nooks-Regular.otf}]{Main Font}
%
\usefonttheme{serif}
\urlstyle{tt}
%
% other official color variations:
% primary: Old original: 1B213E, Light red: FFDEDE, Red: FF4132, Dark red: 410500, Light green: E1FFD9, Green: 0ACD5A, Dark green: 002300
% secondry: Old original: 855C24, Light purple: E3DEFF, Purple: A07DF5, Dark purple: 2D004B, Light blue: CDF0FF, Blue: 32B4E6, Dark blue: 002332

% original color scheme
% \definecolor{SecondaryColor}{HTML}{855C24}
% \definecolor{PrimaryColor}{HTML}{1B213E}

% updated purple color scheme
\definecolor{SecondaryColor}{HTML}{FF4132}
\definecolor{PrimaryColor}{HTML}{2D004B}

% red-brown color scheme
% \definecolor{SecondaryColor}{HTML}{FF4132}
% \definecolor{PrimaryColor}{HTML}{410500}

\setbeamercolor{normal text}{fg=PrimaryColor}
\setbeamercolor{alerted text}{fg=SecondaryColor, bg=PrimaryColor}

\setbeamertemplate{blocks}[rounded]
%
\newcommand{\thankyoupage}[1]{
    \frametitle{#1}
    \includegraphics[width=.4\textwidth]{./corvinus-logos/color_emblem.pdf}
    \hfill{\putemail}
}
\newcommand{\closingframes}[1]{
    \metroset{outer/numbering=none}
    \frame{\thankyoupage{#1}}
}
\newcommand{\simpleopen}{
    \metroset{outer/numbering=none, outer/progressbar=foot}
    \frame{\titlepage}
    \metroset{outer/numbering=counter, outer/progressbar=foot, block=transparent}%
}
\newcommand{\openingframes}[1]{
    \metroset{outer/numbering=none, outer/progressbar=foot}
    \frame{\titlepage}
    \frame{\frametitle{#1}
    \tableofcontents}
    \metroset{outer/numbering=counter, outer/progressbar=foot, block=transparent}%
}
\newcommand{\bibframes}[1]{
    \metroset{outer/numbering=none, outer/progressbar=foot}
    \begin{frame}[allowframebreaks]
	\urlstyle{same}
    	\frametitle{#1}
    	\printbibliography[heading=none]
	\urlstyle{tt}
    \end{frame}
}
\newcommand{\myinstlogo}{./corvinus-logos/color_simple_ENG.pdf}

\endinput
