NextDisc - Next.js Discovery Tool

NextDisc is a lightweight and powerful tool for discovering information about applications built with Next.js. It parses key files and data points to uncover paths, routes, and resources used by the app.

Features


- _buildManifest.js: Contains static route definitions.
- _ssgManifest.js: Lists statically generated routes.
-  _middlewareManifest.js: Provides middleware route information.
-  __NEXT_DATA__: Embedded JSON object with page and query data.
-  routes-manifest.json: Lists all dynamic and static routes.

Installation

Prerequisites

-	Python 3.6+
-	pip (Python package installer)

Install Required Dependencies

```
pip install requests
```

Clone the Repository

```
git clone https://github.com/m0noid/nextdisc.git
cd nextdisc
```

Usage

Basic Usage

Scan a single URL:

```
python3 nextdisc.py https://example.com
```
Scan multiple URLs:

```
python3 nextdisc.py https://example.com https://another-example.com
```
Using a File with URLs

You can pipe a list of URLs from a file:

```
cat urls.txt | python3 nextdisc.py
```

Or redirect input:

```
python3 nextdisc.py < urls.txt
```

Command-Line Options

	-	-o / --output: Write results to a file.

```
python3 nextdisc.py https://example.com -o output.txt
```

	-	-u / --user-agent: Use a custom User-Agent string.

```
python3 nextdisc.py https://example.com -u "MyCustomAgent/1.0"
```

	-	-t / --timeout: Set a timeout for HTTP requests (default: 10 seconds).

```
python3 nextdisc.py https://example.com -t 5
```

	-	-v / --verbose: Enable verbose logging for debugging.

```
python3 nextdisc.py https://example.com -v
```

Examples

Extracting All Routes and Paths

```
python3 nextdisc.py https://example.com
```

Piping Input and Saving to a File

```
cat urls.txt | python3 nextdisc.py -o results.txt
```

Combining Options

```
cat urls.txt | python3 nextdisc.py -v -u "CustomAgent/2.0" -o results.txt
```

Contributing

Contributions are welcome! If you have ideas for new features or improvements, feel free to open an issue or submit a pull request.

Local Development

	1.	Fork the repository.
	2.	Clone your fork:

```
git clone https://github.com/m0noid/nextdisc.git
cd nextdisc
```

	3.	Create a new branch for your feature:

git checkout -b feature-name


	4.	Make your changes and commit:

git commit -m "Add new feature"


	5.	Push to your fork and open a pull request.

License

This project is licensed under the MIT License. See the LICENSE file for details.

Disclaimer

This tool is intended for educational and ethical use only. Ensure you have proper authorization before analyzing any website or application.

Feel free to customize the placeholder https://github.com/m0noid/nextdisc.git with your actual repository URL and modify the details as needed!
