# TypoFix

Python script to fix typography mistakes in **LaTeX** (best suit to Czech).

## Usage

```bash
python typofix.py name_of_the_file
```

Very simple help (so far):

```
python typofix.py -h
```

## Features

It allows to convert this:

```
V. r. 1994 založil v Andách ve výšce 4000 m n. m. Typos a. s.
```
to

```
V.~r. 1994 založil v~Andách ve výšce 4000~m n.~m. Typos a.~s.
```

Or this:

```
Česká ( tzv. Čára ) je betálná brněnská ulica ( s. r. o. ). Spravoval jí prof. Jméno Příjmení, Dr.
```

to

```
Česká (tzv.~Čára) je betálná brněnská ulica (s.~r.~o.). Spravoval jí prof.~Jméno Příjmení,~Dr.
```
