<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body>

<h1>Open Redirect Scanner</h1>

<p>Open Redirect Scanner is a Python tool designed to identify potential open redirect vulnerabilities in URLs. It supports scanning single URLs or multiple URLs from a file with various payloads to detect vulnerabilities.</p>

<h2>Features</h2>
<ul>
    <li>Check if a URL is alive.</li>
    <li>Add request headers and verify if redirected.</li>
    <li>Brute force payloads to find open redirects.</li>
    <li>Read URLs and payloads from files.</li>
    <li>Provide payloads directly through the command line.</li>
</ul>

<h2>Prerequisites</h2>
<p>Python 3.x</p>
<p><code>requests</code> library</p>

<p>Install the <code>requests</code> library using pip:</p>
<pre><code>pip install requests</code></pre>

<h2>Project Structure</h2>
<pre><code>openredirect/
├── includes/
│   ├── scanning.py
│   ├── url_reader.py
│   └── write_and_read.py
├── utils/
│   ├── banner.py
│   └── internet_check.py
├── main.py
├── urls.txt
└── payloads.txt
</code></pre>

<h2>Usage</h2>

<h3>Running the Script</h3>

<p>1. <strong>To process URLs from a file and payloads from a file:</strong></p>
<pre><code>python main.py -f "urls.txt" -p "payloads.txt"</code></pre>

<p>2. <strong>To process a single URL with payloads from a file:</strong></p>
<pre><code>python main.py -u "http://example.com" -p "payloads.txt"</code></pre>

<p>3. <strong>To process a single URL with payloads directly from the command line:</strong></p>
<pre><code>python main.py -u "http://example.com" -pl "payload1,payload2,payload3"</code></pre>

<h3>Command Line Arguments</h3>
<ul>
    <li><code>-u</code>, <code>--url</code> : URL to be processed.</li>
    <li><code>-f</code>, <code>--file</code> : File location of URLs to be processed.</li>
    <li><code>-p</code>, <code>--payload</code> : File location of payloads to be used.</li>
   
</ul>

</body>
</html>