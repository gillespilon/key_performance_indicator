# Key performance indicator (KPI)

## In brevi

Office workers create, update, and publish documents. Whether it's creating presentations, responding to emails, or doing statistical analysis, they are creating documents. Unlike a manufacturing environment, their output appears invisible to an observer of their work process. If such a worker were to commit their documents to a Git repository, they could make their work visible . These commits could then be reported as a key performance indicator (KPI).

## Data

The data file is available [here (kpis.csv)](https://drive.google.com/file/d/0BzrdQfHR2I5Dc0o5X3puNHUxdTQ/view?usp=sharing). It consists of a date column and six KPI data columns. Dates are entered using [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) date format (yyyy-mm-dd). The KPI columns are the number of commits per KPI.

## Methodology

A Git "commit" is a recorded change to a repository. Each day an office worker determines the number of commits made for each repository, records the values in the kpis.csv file, and executes kpis.py or kpis.ipynb. A graph of individual commits v. date and a graph of total commits v. date are created and saved in svg and pdf formats.

## License

Copyright (c) 2017 GILLES PILON <gillespilon@gmail.com>

Permission to use, copy, modify, and distribute this software for any purpose with or without fee is hereby granted, provided that the above copyright notice and this permission notice appear in all copies.

THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
