% hunthesis.cls
% A LaTeX class for Hungarian dual-institution academic theses
% Based on the ELTE / Budapesti Corvinus Egyetem thesis style
% ---------------------------------------------------------------

\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{hunthesis}[2026/06/01 Hungarian Dual-Institution Thesis Class]

% ---------------------------------------------------------------
% BASE CLASS & OPTIONS
% ---------------------------------------------------------------
\DeclareOption{12pt}{\PassOptionsToClass{12pt}{article}}
\DeclareOption{11pt}{\PassOptionsToClass{11pt}{article}}
\DeclareOption*{\PassOptionsToClass{\CurrentOption}{article}}
\ExecuteOptions{12pt}
\ProcessOptions\relax
\LoadClass[a4paper]{article}

% ---------------------------------------------------------------
% REQUIRED PACKAGES
% ---------------------------------------------------------------
\RequirePackage[T1]{fontenc}
\RequirePackage[utf8]{inputenc}
\RequirePackage[hungarian]{babel}   % swap order if writing in English
\usepackage[backend=biber, style=apa]{biblatex}
\usepackage{csquotes}
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
\RequirePackage{ifthen}
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
\RequirePackage{bookmark}

% Title
\newcommand{\thesistitle}[1]{\def\@thesistitle{#1}}
\newcommand{\thesissubtitle}[1]{\def\@thesissubtitle{#1}}

% Author block
\newcommand{\authorname}   [1]{\def\@authorname{#1}}
\newcommand{\authorprogram}[1]{\def\@authorprogram{#1}}

% Supervisor block
\newcommand{\supervisorname} [1]{\def\@supervisorname{#1}}
\newcommand{\supervisortitle}[1]{\def\@supervisortitle{#1}}

% Institutions
\newcommand{\institution} [1]{\def\@institution{#1}}

% Logo file paths (leave empty to omit)
\newcommand{\logo} [1]{\def\@logo{#1}}

% Year
\newcommand{\thesisyear}[1]{\def\@thesisyear{#1}}

% Sensible defaults so the template compiles even without configuration
\thesistitle    {Thesis Title}
\authorname     {Author Name}
\authorprogram  {Programme Name}
\supervisorname {Supervisor Name}
\supervisortitle{Associate Professor}
\institution    {Institution \\Faculty Name}
\logo{}    % set to a file path, e.g. {logo-left.png}
\thesisyear     {\the\year}

\hypersetup{
  colorlinks  = false,
  pdftitle    = {\@thesistitle},
  pdfauthor   = {\@authorname},
  bookmarksnumbered = true,
}

% Titlepage
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

    \vspace*{.5cm}
    \begin{center}
      {\huge\bfseries\@thesistitle\par}
      \vspace{1cm}
      \Large \bfseries\@thesissubtitle\par
    \end{center}

    \vspace{3cm}

    \hfill
    \begin{minipage}[t]{0.5\textwidth}
        {\Large\bfseries Készítette:}\par
        \vspace{0.6em}
        {\Large \@authorname}\par
        \vspace{0.4em}
        {\normalsize \@authorprogram}
    \end{minipage}
    \begin{minipage}[t]{0.4\textwidth}
      {\Large\bfseries Témavezető:}\par
      \vspace{0.6em}
      {\Large \@supervisorname}\par
      \vspace{0.4em}
      {\normalsize \@supervisortitle}
    \end{minipage}
    \hfill

    \vfill

    \begin{center}
      \begin{minipage}[t]{0.50\textwidth}
        \begin{center}
          \includegraphics[height=5cm]{\@logo}

          % {\large \@institution}
        \end{center}
      \end{minipage}
    \end{center}

    \vspace{1.5cm}

    \begin{center}
      {\large\bfseries \@thesisyear}
    \end{center}

    \cleardoublepage
    
    \thispagestyle{empty}
    \setlength{\parindent}{0pt}

    \tableofcontents
    \cleardoublepage
  \end{titlepage}
}

\newtheorem{theorem}   {Tétel}   [section]
\newtheorem{lemma}     {Lemma}   [section]
\newtheorem{corollary} {Következmény}[section]
\newtheorem{proposition}{Állítás}[section]

\theoremstyle{definition}
\newtheorem{definition}{Definíció}[section]
\newtheorem{example}   {Példa}   [section]
\newtheorem{remark}    {Megjegyzés}[section]

\onehalfspacing

\endinput
