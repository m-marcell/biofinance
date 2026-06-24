% bce-thesis.cls

\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{bce-thesis}[2026/06/01 Budapesti Corvinus Egyetem szakdolgozati sablon]

\DeclareOption{12pt}{\PassOptionsToClass{12pt}{article}}
\DeclareOption{11pt}{\PassOptionsToClass{11pt}{article}}
\DeclareOption*{\PassOptionsToClass{\CurrentOption}{article}}
\ExecuteOptions{12pt}
\ProcessOptions\relax
\LoadClass[a4paper]{article}

\RequirePackage[T1]{fontenc}
\RequirePackage[utf8]{inputenc}
\RequirePackage[hungarian]{babel}
\usepackage{csquotes}
\usepackage[backend=biber, style=apa]{biblatex}
\RequirePackage{lmodern}
\RequirePackage{microtype}

\RequirePackage{geometry}
\geometry{
  a4paper,
  top    = 2.5cm,
  bottom = 2.5cm,
  left   = 3.0cm,
  right  = 2.5cm,
}

\RequirePackage{graphicx}
\RequirePackage{xcolor}
% \RequirePackage{ifthen}
\RequirePackage{etoolbox}
\RequirePackage{setspace}
\RequirePackage{titlesec}
\RequirePackage{titletoc}
\RequirePackage{fancyhdr}
\RequirePackage{emptypage}       % suppresses headers on truly blank pages
\RequirePackage{booktabs}
\RequirePackage{array}
\RequirePackage{longtable}
\RequirePackage{multirow}
\RequirePackage{caption}
\RequirePackage{subcaption}
\RequirePackage{amsmath}
\RequirePackage{amssymb}
\RequirePackage{amsthm}
\RequirePackage{mathtools}
\RequirePackage{hyperref}
% \RequirePackage{bookmark}

\onehalfspacing

\newcommand{\thesistitle}[1]{\def\@thesistitle{#1}}
\newcommand{\thesissubtitle}[1]{\def\@thesissubtitle{#1}}

\newcommand{\authorname}[1]{\def\@authorname{#1}}
\newcommand{\authorprogram}[1]{\def\@authorprogram{#1}}

\newcommand{\supervisorname}[1]{\def\@supervisorname{#1}}
\newcommand{\supervisortitle}[1]{\def\@supervisortitle{#1}}

\newcommand{\institution}[1]{\def\@institution{#1}}
\newcommand{\logo}[1]{\def\@logo{#1}}
\newcommand{\city}[1]{\def\@city{#1}}
\newcommand{\thesisyear}[1]{\def\@thesisyear{#1}}

\newcommand{\nyilatkozatdatum}[1]{\def\@nyilatkozatdatum{#1}}

\thesistitle{Főcím}
\thesissubtitle{Alcím (opcionális)}
\authorname{Alfonz Aladár}
\authorprogram{Képzés\\Specializáció (opcionális)}
\supervisorname{Dr. Cirmai Cecília}
\supervisortitle{Egyetemi Tanár}
\institution{Budapesti Corvinus Egyetem}
\city{Budapest}
\thesisyear{\the\year}
\nyilatkozatdatum{\today}

\hypersetup{
  colorlinks  = false,
  pdftitle    = {\@thesistitle},
  pdfauthor   = {\@authorname},
}

\renewcommand{\maketitle}{
	\begin{titlepage}
		\thispagestyle{empty}
		\setlength{\parindent}{0pt}

		\vspace*{3cm}

		\begin{center}
				\Huge \bfseries SZAKDOLGOZAT\par
				\vspace{2cm}
				\Large \bfseries \@authorname

				\vfill

				{\large\bfseries \@thesisyear}
		\end{center}

		\cleardoublepage

		\thispagestyle{empty}
		\setlength{\parindent}{0pt}

		\vspace*{1cm}

		\begin{center}
			{\Huge\bfseries\@thesistitle\par}
			\vspace{1cm}
			\Large \bfseries\@thesissubtitle\par
		\end{center}

		\vspace{3cm}

		\hfill
		\begin{minipage}[t]{0.5\textwidth}
			{\Large\bfseries Készítette:}\par
			\vspace{0.2cm}
			{\Large \@authorname}\par
			\vspace{0.1cm}
			{\normalsize \@authorprogram}
		\end{minipage}
		\begin{minipage}[t]{0.4\textwidth}
			{\Large\bfseries Témavezető:}\par
			\vspace{0.2cm}
			{\Large \@supervisorname}\par
			\vspace{0.1cm}
			{\normalsize \@supervisortitle}
		\end{minipage}
		\hfill

		\vfill

		\begin{center}
			\includegraphics[height=5cm]{\@logo}
		\end{center}

		\vspace{1.5cm}

		\begin{center}
				{\large\bfseries \@city, \@thesisyear}
		\end{center}

		\cleardoublepage

		\thispagestyle{empty}
		\setlength{\parindent}{0pt}

		\tableofcontents
		\cleardoublepage
	\end{titlepage}
}



\newcommand{\nyilatkozat}{
	\begin{center}
	    \huge \textbf{Nyilatkozat}
	\end{center}
	\addcontentsline{toc}{section}{Nyilatkozat}

	\bigskip

% Nyilatkozat szövege

	Alulírott \textbf{\emph{\@authorname}}, büntetőjogi felelősségem tudatában kijelentem, hogy az általam benyújtott, \textbf{\emph{\@thesistitle}} című szakdolgozat önálló szellemi termékem. Amennyiben mások munkáját felhasználtam, azokra megfelelően hivatkozom, beleértve a nyomtatott és az internetes forrásokat is.\par

	\bigskip

	\begin{flushleft}
		\@city, \@nyilatkozatdatum
	\end{flushleft}
}

\newcommand{\initial}[1]{\LARGE{#1}\normalsize}

\newtheorem{theorem}{Tétel}[section]
\newtheorem{lemma}{Lemma}[section]
\newtheorem{corollary}{Következmény}[section]
\newtheorem{proposition}{Állítás}[section]

\theoremstyle{definition}
\newtheorem{definition}{Definíció}[section]
\newtheorem{example}{Példa}[section]
\newtheorem{remark}{Megjegyzés}[section]

\endinput
