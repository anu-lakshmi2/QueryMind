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

function formatSQL(sql) {
    const keywords = ["SELECT", "FROM", "JOIN", "ON", "WHERE", "AND", "OR", 
                      "ORDER BY", "GROUP BY", "HAVING", "LIMIT"];
    let formatted = sql;
    keywords.forEach(keyword => {
        const regex = new RegExp(`\\b${keyword}\\b`, 'gi');
        formatted = formatted.replace(regex, `\n${keyword}`);
    });
    return formatted.trim();
}

async function handleSubmit() {
    const text = queryInput.value.trim();
    if (text === "") return;

    errorBox.classList.add("hidden");
    // Animate hero image out
    document.getElementById("heroImage").classList.add("slide-up");
    resultsSection.classList.add("hidden");
    explanationSection.classList.add("hidden");

    const data = await runQuery(text);
    console.log("Success:", data.success, "Error:", data.error);

    if (!data.success) {
    errorBox.textContent = data.error || "Something went wrong.";
    errorBox.classList.remove("hidden");
    resultsSection.classList.add("hidden");
    explanationSection.classList.add("hidden");
    return;
}
    document.getElementById("heroImage").classList.add("slide-up");
    lastResults = data.rows;
    addToHistory(text);
    renderTable(data.rows);
    sqlBox.textContent = formatSQL(data.sql);
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

const historyList = document.getElementById("historyList");
const historySearch = document.getElementById("historySearch");
const newChatBtn = document.getElementById("newChatBtn");

let queryHistory = [];

function addToHistory(text) {
    queryHistory.unshift(text);  // add to top
    renderHistory(queryHistory);
}

function renderHistory(items) {
    historyList.innerHTML = "";
    items.forEach(item => {
        const div = document.createElement("div");
        div.className = "history-item";
        div.textContent = item;
        div.addEventListener("click", () => {
            queryInput.value = item;
            handleSubmit();
        });
        historyList.appendChild(div);
    });
}

historySearch.addEventListener("input", () => {
    const filtered = queryHistory.filter(q =>
        q.toLowerCase().includes(historySearch.value.toLowerCase())
    );
    renderHistory(filtered);
});

newChatBtn.addEventListener("click", () => {
    queryInput.value = "";
    resultsSection.classList.add("hidden");
    explanationSection.classList.add("hidden");
    errorBox.classList.add("hidden");
    document.getElementById("heroImage").classList.remove("slide-up");
});