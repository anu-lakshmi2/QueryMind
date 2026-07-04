const queryInput = document.getElementById("queryInput");
const submitBtn = document.getElementById("submitBtn");
const resultsSection = document.getElementById("resultsSection");
const resultsTable = document.getElementById("resultsTable");
const sqlBox = document.getElementById("sqlBox");
const explanationSection = document.getElementById("explanationSection");
const explanationText = document.getElementById("explanationText");
const errorBox = document.getElementById("errorBox");
const downloadBtn = document.getElementById("downloadBtn");

let lastResults = [];  // we'll store the latest results here for CSV download

async function runQuery(text) {
    try {
        const response = await fetch("http://127.0.0.1:8000/query", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ text: text })
        });

        const data = await response.json();
        return data;

    } catch (error) {
        return { success: false, error: "Could not connect to server." };
    }
}

function renderTable(rows) {
    if (rows.length === 0) {
        resultsTable.innerHTML = "<tr><td>No results found.</td></tr>";
        return;
    }

    const columns = Object.keys(rows[0]);

    let html = "<tr>";
    columns.forEach(col => {
        html += `<th>${col}</th>`;
    });
    html += "</tr>";

    rows.forEach(row => {
        html += "<tr>";
        columns.forEach(col => {
            html += `<td>${row[col]}</td>`;
        });
        html += "</tr>";
    });

    resultsTable.innerHTML = html;
}

function buildExplanation(parsed, sql) {
    const tables = parsed.tables.join(", ");
    let explanation = `This was interpreted as a ${parsed.intent} query on the "${tables}" table`;

    if (parsed.conditions.length > 0 || parsed.text_matches.length > 0) {
        explanation += " with a filtering condition applied";
    }

    explanation += `. The generated SQL was: ${sql}`;
    return explanation;
}

function downloadCSV(rows) {
    if (rows.length === 0) return;

    const columns = Object.keys(rows[0]);
    const header = columns.join(",");
    const rowLines = rows.map(row =>
        columns.map(col => `"${row[col]}"`).join(",")
    );

    const csv = [header, ...rowLines].join("\n");
    const blob = new Blob([csv], { type: "text/csv" });
    const url = URL.createObjectURL(blob);

    const a = document.createElement("a");
    a.href = url;
    a.download = "querymind_results.csv";
    a.click();
    URL.revokeObjectURL(url);
}


async function handleSubmit() {
    const text = queryInput.value.trim();
    if (text === "") return;

    errorBox.classList.add("hidden");
    resultsSection.classList.add("hidden");
    explanationSection.classList.add("hidden");

    const data = await runQuery(text);

    if (!data.success) {
        errorBox.textContent = data.error || "Something went wrong.";
        errorBox.classList.remove("hidden");
        return;
    }

    lastResults = data.rows;
    renderTable(data.rows);
    sqlBox.textContent = data.sql;
    explanationText.textContent = buildExplanation(data.parsed, data.sql);

    resultsSection.classList.remove("hidden");
    explanationSection.classList.remove("hidden");
}

submitBtn.addEventListener("click", handleSubmit);

queryInput.addEventListener("keypress", function(e) {
    if (e.key === "Enter") {
        handleSubmit();
    }
});


downloadBtn.addEventListener("click", () => downloadCSV(lastResults));