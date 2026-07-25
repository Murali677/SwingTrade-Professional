import os
from config import OUTPUT_FOLDER


def create_html_report(results):

    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

    report_file = os.path.join(
        OUTPUT_FOLDER,
        "SwingTradeReport.html"
    )

    html = """
<!DOCTYPE html>
<html>
<head>

<meta charset="UTF-8">

<title>Swing Trade Scanner</title>

<style>

body{
font-family:Arial;
background:#f4f6f9;
padding:25px;
}

h1{
text-align:center;
color:#0d47a1;
}

table{
width:100%;
border-collapse:collapse;
background:white;
box-shadow:0 2px 10px rgba(0,0,0,.15);
}

th{
background:#1565C0;
color:white;
padding:12px;
position:sticky;
top:0;
}

td{
padding:10px;
text-align:center;
border-bottom:1px solid #ddd;
}

tr:nth-child(even){
background:#f7f7f7;
}

tr:hover{
background:#e3f2fd;
}

.buy{
background:#43A047;
color:white;
padding:5px 10px;
border-radius:15px;
font-weight:bold;
}

.strong{
background:#1B5E20;
color:white;
padding:5px 10px;
border-radius:15px;
font-weight:bold;
}

.watch{
background:#FB8C00;
color:white;
padding:5px 10px;
border-radius:15px;
font-weight:bold;
}

.ignore{
background:#9E9E9E;
color:white;
padding:5px 10px;
border-radius:15px;
font-weight:bold;
}

.score{
font-weight:bold;
color:#1565C0;
}

a{
text-decoration:none;
padding:6px 12px;
background:#1565C0;
color:white;
border-radius:6px;
}

a:hover{
background:#0d47a1;
}

.summary{

background:white;

padding:20px;

margin-bottom:20px;

box-shadow:0 2px 10px rgba(0,0,0,.15);

}

</style>

</head>

<body>

<h1>📈 Nifty 100 Swing Trade Scanner</h1>
"""

    strong = len([x for x in results if x["Signal"] == "Strong Buy"])
    buy = len([x for x in results if x["Signal"] == "Buy"])
    watch = len([x for x in results if x["Signal"] == "Watch"])

    html += f"""
<div class="summary">

<h3>Summary</h3>

<b>Stocks Scanned :</b> {len(results)}<br><br>

<b>Strong Buy :</b> {strong}<br>

<b>Buy :</b> {buy}<br>

<b>Watch :</b> {watch}

</div>

<table>

<tr>

<th>Rank</th>

<th>Stock</th>

<th>CMP</th>

<th>Entry</th>

<th>Target</th>

<th>Stop Loss</th>

<th>Score</th>

<th>Reason</th>

<th>Signal</th>

<th>TradingView</th>

<th>Screener</th>

</tr>

"""

    for i, stock in enumerate(results, start=1):

        signal_class = "ignore"

        if stock["Signal"] == "Strong Buy":
            signal_class = "strong"

        elif stock["Signal"] == "Buy":
            signal_class = "buy"

        elif stock["Signal"] == "Watch":
            signal_class = "watch"

        html += f"""

<tr>

<td>{i}</td>

<td><b>{stock['Symbol']}</b></td>

<td>₹{stock['CMP']}</td>

<td>₹{stock['Entry']}</td>

<td>₹{stock['Target']}</td>

<td>₹{stock['StopLoss']}</td>

<td class="score">{stock['Score']}</td>

<td>{stock['Reasons']}</td>

<td><span class="{signal_class}">{stock['Signal']}</span></td>

<td>
<a href="{stock['TradingView']}" target="_blank">
Chart
</a>
</td>

<td>
<a href="{stock['Screener']}" target="_blank">
Open
</a>
</td>

</tr>

"""

    html += """

</table>

</body>

</html>

"""

    with open(report_file, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"\nHTML Report Created : {report_file}")

    return report_file