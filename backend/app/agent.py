from langchain.tools import tool
from backend.app.drive_tool import search_drive
from datetime import datetime, timedelta,timezone

@tool
def drive_search_tool(user_query: str):
    """
    Search files in Google Drive using Google Drive API q queries.
    """

    lower_query = user_query.lower()
    query_parts = ["trashed=false"]

   
    if "pdf" in lower_query:

        query_parts.append(
            "mimeType='application/pdf'"
        )

    if (
        "image" in lower_query
        or "photo" in lower_query
        or "pics" in lower_query
        or "picture" in lower_query
    ):

        query_parts.append(
            "mimeType contains 'image/'"
        )

    if (
        "sheet" in lower_query
        or "excel" in lower_query
        or "spreadsheet" in lower_query
    ):
        query_parts.append("mimeType='application/vnd.google-apps.spreadsheet'")
    if (
        "doc" in lower_query
        or "document" in lower_query
    ):
        query_parts.append(
            "mimeType='application/vnd.google-apps.document'"
        )

    if "folder" in lower_query:
        query_parts.append(
            "mimeType='application/vnd.google-apps.folder'"
        )


    # exact name search
    if "exact" in lower_query:
        filename = (
            lower_query
            .replace("exact", "")
            .strip()
        )
        query_parts.append(
            f"name='{filename}'"
        )

    # partial name search
    name_keywords = [
        "report",
        "invoice",
        "employee",
        "daily",
        "party",
        "image",
        "salary",
        "attendance",
        "resume",
        "notes"
    ]

    for keyword in name_keywords:
        if keyword in lower_query:
            query_parts.append(
                f"name contains '{keyword}'"
            )

    # full text search
    fulltext_keywords = [
        "marketing",
        "finance",
        "budget",
        "revenue",
        "analysis",
        "strategy",
        "sales",
        "performance"
    ]

    for keyword in fulltext_keywords:
        if keyword in lower_query:
            query_parts.append(
                f"fullText contains '{keyword}'"
            )

    # generic search fallback
    if len(query_parts) == 1:
        search_terms = lower_query.split()
        ignored_words = [
            "find",
            "give",
            "show",
            "me",
            "the",
            "all",
            "files",
            "file"
        ]
        for term in search_terms:
            if (
                len(term) > 2
                and term not in ignored_words
            ):
                query_parts.append(
                    f"name contains '{term}'"
                )

    # date filters
    today = datetime.now(timezone.utc)

    # Today
    if "today" in lower_query:
        today_str = today.strftime(
            "%Y-%m-%dT00:00:00"
        )
        query_parts.append(
            f"modifiedTime > '{today_str}'"
        )

    # Yesterday
    if "yesterday" in lower_query:
        yesterday = today - timedelta(days=1)
        yesterday_str = yesterday.strftime(
            "%Y-%m-%dT00:00:00"
        )
        today_str = today.strftime(
            "%Y-%m-%dT00:00:00"
        )
        query_parts.append(
            f"modifiedTime > '{yesterday_str}'"
        )

    # Last week
    if "last week" in lower_query:
        last_week = today - timedelta(days=7)
        last_week_str = last_week.strftime(
            "%Y-%m-%dT00:00:00"
        )

        query_parts.append(
            f"modifiedTime > '{last_week_str}'"
        )

    # This month
    if "this month" in lower_query:
        first_day = today.replace(day=1)
        month_str = first_day.strftime(
            "%Y-%m-%dT00:00:00"
        )
        query_parts.append(
            f"modifiedTime > '{month_str}'"
        )

    # final query 
    query = " and ".join(query_parts)
    print("\nGenerated Drive Query:")
    print(query)

    files = search_drive(query)

    if not files:
        return "No matching files found."

    output = ["# Files Found\n"]

    for file in files:
        # Folder link
        if (
            file["mimeType"]
            == "application/vnd.google-apps.folder"
        ):
            link = (
                "https://drive.google.com/drive/folders/"
                f"{file['id']}"
            )

        else:
            link = (
                "https://drive.google.com/file/d/"
                f"{file['id']}/view"
            )

        output.append(
            f"""
                ## 📄 {file['name']}

                - Type: {file['mimeType']}
                - Modified: {file['modifiedTime']}
                - Link: {link}
            """
        )

    return "\n".join(output)