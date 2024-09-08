from langchain.tools import StructuredTool
from schemas.schema import WriteReportArgsSchema


def write_report(filename, html):
    """Function to create html file with html string"""

    if not isinstance(html, str):
        html = html.get('html')

    with open(filename, "w") as f:
        f.write(html)


# tool - write_report
write_report_tool = StructuredTool.from_function(
    name="write_report",
    description="Write an HTML file to disk. Use this tool whenever someone asks for a report.",
    func=write_report,
    args_schema=WriteReportArgsSchema,
)
