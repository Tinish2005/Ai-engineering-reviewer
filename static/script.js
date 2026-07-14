async function runReview() {
    const code = document.getElementById("codeInput").value.trim();
    const container = document.getElementById("output");
    container.innerHTML = "";

    if (!code) {
        showLoading(container, "Please paste code first.");
        return;
    }

    showLoading(container, "Running engineering review...");

    try {
        const res = await fetch("/review", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ code })
        });

        const result = await res.json();

        container.innerHTML = "";

        if (result.type === "error") {
            container.innerHTML =
                "<p class=\"loading-text\">" +
                escapeHtml(result.message || "Error") +
                "</p>";
            return;
        }

        renderComponents(
            result.components,
            container
        );

        loadHistory();

    } catch (err) {

        container.innerHTML = "";

        showLoading(
            container,
            "Review failed. Please try again."
        );
    }
}

async function runRefactor() {
    const code = document.getElementById("codeInput").value.trim();
    const container = document.getElementById("output");

    if (!code) {
        alert("Please paste code before refactoring.");
        return;
    }

    const loading = document.createElement("p");
    loading.textContent = "Generating refactored code...";
    loading.className = "loading-text";
    container.appendChild(loading);

    try {
        const res = await fetch("/refactor", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ code })
        });
        const component = await res.json();
        container.removeChild(loading);
        renderComponents([component], container);
    } catch (err) {
        loading.textContent = "Refactor failed. Please try again.";
    }
}


function showLoading(container, message) {
    const loading = document.createElement("p");
    loading.className = "loading-text";
    loading.textContent = message;
    container.appendChild(loading);
}


function renderComponents(components, container) {
    if (!components || !components.length) {
        showLoading(container, "No components returned.");
        return;
    }
    components.forEach(function(c) {
        switch (c.type) {
            case "score_card":      renderScoreCard(c, container); break;
            case "metric_card":     renderMetricCard(c, container); break;
            case "complexity_card": renderComplexityCard(c, container); break;
            case "finding_list":    renderFindingList(c, container); break;
            case "rule_check_card": renderRuleCheckCard(c, container); break;
            case "list":            renderList(c, container); break;
            case "card":            renderSimpleCard(c, container); break;
            case "ai_summary":      renderAISummary(c, container); break;
            case "code_card":       renderCodeCard(c, container); break;
            case "diff_card":       renderDiffCard(c, container); break;
            default:                renderUnknown(c, container); break;
        }
    });
}

async function loadHistory() {

    try {

        const res =
            await fetch("/history");

        const rows =
            await res.json();

        const panel =
            document.getElementById(
                "historyPanel"
            );

        if (!panel) {
            return;
        }

        panel.innerHTML = "";

        if (!rows.length) {

            panel.innerHTML =
                `
                <div class="card">
                    No reviews yet.
                </div>
                `;

            return;
        }

        rows.forEach(r => {

            panel.innerHTML += `
                <div class="card history-card">
                    <strong>${r.language}</strong>
                    <br>
                    Score:
                    <strong>${r.score}</strong>
                    <br>
                    ${r.created_at}
                </div>
            `;
        });

    } catch (err) {

        console.error(err);

        const panel =
            document.getElementById(
                "historyPanel"
            );

        if (panel) {
            panel.innerHTML =
                `
                <div class="card">
                    Failed to load history.
                </div>
                `;
        }
    }
}

function renderScoreCard(c, container) {
    const el = document.createElement("div");
    el.className = "card score-card";

    const overall = c.overall != null ? c.overall : 0;
    const verdict = c.verdict || "";

    let scoreClass = "score-critical";
    if (overall >= 90) scoreClass = "score-excellent";
    else if (overall >= 75) scoreClass = "score-good";
    else if (overall >= 60) scoreClass = "score-acceptable";
    else if (overall >= 40) scoreClass = "score-needs-work";

    const catRows = (c.categories || []).map(function(cat) {
        const catScore = cat.score != null ? cat.score : 0;
        let barClass = "bar-critical";
        if (catScore >= 90) barClass = "bar-excellent";
        else if (catScore >= 75) barClass = "bar-good";
        else if (catScore >= 60) barClass = "bar-acceptable";
        else if (catScore >= 40) barClass = "bar-needs-work";

        return "<div class=\"score-cat-row\">" +
            "<div class=\"score-cat-header\">" +
                "<span class=\"score-cat-name\">" + escapeHtml(cat.name) + "</span>" +
                "<span class=\"score-cat-weight\">weight " + escapeHtml(String(cat.weight_pct)) + "%</span>" +
                "<span class=\"score-cat-value\">" + escapeHtml(String(catScore)) + "</span>" +
            "</div>" +
            "<div class=\"score-bar-track\"><div class=\"score-bar-fill " + barClass + "\" style=\"width: " + catScore + "%\"></div></div>" +
            "</div>";
    }).join("");

    el.innerHTML =
        "<h3>" + escapeHtml(c.title) + "</h3>" +
        "<div class=\"score-hero " + scoreClass + "\">" +
            "<div class=\"score-hero-number\">" + escapeHtml(String(overall)) + "</div>" +
            "<div class=\"score-hero-details\">" +
                (c.language ? "<div class=\"score-hero-lang\">" + escapeHtml(c.language) + "</div>" : "") +
                "<div class=\"score-hero-outof\">out of 100</div>" +
                "<div class=\"score-hero-verdict\">" + escapeHtml(verdict) + "</div>" +
            "</div>" +
        "</div>" +
        "<div class=\"score-categories\">" + catRows + "</div>";

    container.appendChild(el);
}


function renderMetricCard(c, container) {
    const el = document.createElement("div");
    el.className = "card";
    const rows = Object.entries(c.data || {}).map(function(entry) {
        return "<div class=\"metric-row\"><span class=\"metric-key\">" + escapeHtml(entry[0]) + "</span><span class=\"metric-value\">" + escapeHtml(String(entry[1])) + "</span></div>";
    }).join("");
    el.innerHTML = "<h3>" + escapeHtml(c.title) + "</h3><div class=\"metrics-grid\">" + rows + "</div>";
    container.appendChild(el);
}


function renderComplexityCard(c, container) {
    const el = document.createElement("div");
    el.className = "card";

    const cognitive = c.per_function_cognitive || [];
    const cognitiveByKey = {};
    cognitive.forEach(function(f) { cognitiveByKey[f.name + "|" + f.line] = f.value; });

    const rows = (c.per_function_cyclomatic || []).map(function(fn) {
        const cog = cognitiveByKey[fn.name + "|" + fn.line];
        return "<tr><td>" + escapeHtml(fn.name) + "</td><td>" + escapeHtml(String(fn.line)) + "</td><td>" + escapeHtml(String(fn.value)) + "</td><td>" + escapeHtml(String(cog != null ? cog : "-")) + "</td></tr>";
    }).join("");

    const tableHtml = rows
        ? "<table class=\"fn-table\"><thead><tr><th>Function</th><th>Line</th><th>Cyclomatic</th><th>Cognitive</th></tr></thead><tbody>" + rows + "</tbody></table>"
        : "<p>No functions detected.</p>";

    el.innerHTML =
        "<h3>" + escapeHtml(c.title) + "</h3>" +
        "<p><strong>Verdict:</strong> " + escapeHtml(c.verdict) +
        " | Max cyclomatic: " + escapeHtml(String(c.cyclomatic_max)) +
        " | Max cognitive: " + escapeHtml(String(c.cognitive_max)) + "</p>" +
        tableHtml +
        renderFindingsInner(c.findings || []);
    container.appendChild(el);
}


function renderFindingList(c, container) {
    const el = document.createElement("div");
    el.className = "card";
    const covLine = (c.docstring_coverage_pct != null)
        ? "<p><strong>Docstring coverage:</strong> " + escapeHtml(String(c.docstring_coverage_pct)) + "%</p>"
        : "";
    el.innerHTML = "<h3>" + escapeHtml(c.title) + "</h3>" + covLine + renderFindingsInner(c.findings || []);
    container.appendChild(el);
}


function renderRuleCheckCard(c, container) {
    const el = document.createElement("div");
    el.className = "card";

    const total = c.rules_checked || 0;
    const passed = c.rules_passed || 0;
    const passPct = total > 0 ? Math.round((passed / total) * 100) : 0;
    const passClass = passPct === 100 ? "rule-pass-full" : (passPct >= 60 ? "rule-pass-mid" : "rule-pass-low");

    const ruleRows = (c.results || []).map(function(r) {
        const badge = r.status === "pass"
            ? "<span class=\"rule-badge pass\">PASS</span>"
            : "<span class=\"rule-badge fail\">FAIL</span>";
        const count = (r.findings || []).length;
        const countText = count > 0 ? " (" + count + " violation" + (count === 1 ? "" : "s") + ")" : "";
        return "<div class=\"rule-row\">" +
            badge +
            "<span class=\"rule-name\">" + escapeHtml(r.rule) + "</span>" +
            "<span class=\"rule-threshold\">threshold: " + escapeHtml(String(r.threshold)) + "</span>" +
            "<span class=\"rule-finding-count\">" + escapeHtml(countText) + "</span>" +
            "</div>";
    }).join("");

    const allFindings = [];
    (c.results || []).forEach(function(r) {
        if (r.findings) {
            r.findings.forEach(function(f) { allFindings.push(f); });
        }
    });

    el.innerHTML =
        "<h3>" + escapeHtml(c.title) + "</h3>" +
        "<p class=\"rule-summary " + passClass + "\"><strong>" + passed + " / " + total + " rules passed</strong></p>" +
        "<div class=\"rule-list\">" + ruleRows + "</div>" +
        (allFindings.length > 0 ? "<h4>Violations</h4>" + renderFindingsInner(allFindings) : "");
    container.appendChild(el);
}


function renderFindingsInner(findings) {
    if (!findings.length) {
        return "<p class=\"no-findings\">No issues detected.</p>";
    }
    const items = findings.map(function(f) {
        const line = (f.location && f.location.line) ? "Line " + f.location.line : "";
        const sev = escapeHtml(f.severity || "info");
        return "<div class=\"finding severity-" + sev + "\">" +
            "<div class=\"finding-header\">" +
            "<span class=\"finding-title\">" + escapeHtml(f.title || "Finding") + "</span>" +
            "<span class=\"finding-meta\">" + escapeHtml(sev) + (line ? " . " + escapeHtml(line) : "") + "</span>" +
            "</div>" +
            "<div class=\"finding-body\">" +
            "<div><strong>Reason:</strong> " + escapeHtml(f.reason || "") + "</div>" +
            "<div><strong>Impact:</strong> " + escapeHtml(f.impact || "") + "</div>" +
            "<div><strong>Recommendation:</strong> " + escapeHtml(f.recommendation || "") + "</div>" +
            "</div>" +
            "</div>";
    }).join("");
    return "<div class=\"findings-list\">" + items + "</div>";
}


function renderList(c, container) {
    const el = document.createElement("div");
    el.className = "card";
    const items = (c.items || []).map(function(i) {
        const text = typeof i === "string" ? i : JSON.stringify(i);
        return "<li>" + escapeHtml(text) + "</li>";
    }).join("");
    el.innerHTML = "<h3>" + escapeHtml(c.title) + "</h3><ul>" + (items || "<li>No items</li>") + "</ul>";
    container.appendChild(el);
}


function renderSimpleCard(c, container) {
    const el = document.createElement("div");
    el.className = "card";
    el.innerHTML = "<h3>" + escapeHtml(c.title) + "</h3><pre>" + escapeHtml(JSON.stringify(c.data, null, 2)) + "</pre>";
    container.appendChild(el);
}


function renderAISummary(c, container) {
    const el = document.createElement("div");
    el.className = "card";

    const formatItem = function(item) {
        if (typeof item === "string") return "<li>" + escapeHtml(item) + "</li>";
        if (item && typeof item === "object") {
            const parts = [];
            for (const key of Object.keys(item)) {
                parts.push("<strong>" + escapeHtml(key) + ":</strong> " + escapeHtml(String(item[key])));
            }
            return "<li>" + parts.join("<br>") + "</li>";
        }
        return "<li>" + escapeHtml(String(item)) + "</li>";
    };

    const priority = (c.priority_issues || []).map(formatItem).join("");
    const suggestions = (c.suggestions || []).map(formatItem).join("");

    el.innerHTML =
        "<h3>" + escapeHtml(c.title) + "</h3>" +
        "<p>" + escapeHtml(c.summary || "") + "</p>" +
        "<h4>Priority Issues</h4>" +
        "<ul>" + (priority || "<li>No priority issues</li>") + "</ul>" +
        "<h4>Suggestions</h4>" +
        "<ul>" + (suggestions || "<li>No suggestions</li>") + "</ul>";
    container.appendChild(el);
}


function renderCodeCard(component, container) {
    const wrapper = document.createElement("div");
    wrapper.className = "card code-card";
    wrapper.innerHTML =
        "<h3>" + escapeHtml(component.title) + "</h3>" +
        "<pre class=\"code-block\"><code>" + escapeHtml(component.code || "") + "</code></pre>";
    container.appendChild(wrapper);
}


function renderDiffCard(c, container) {
    const el = document.createElement("div");
    el.className = "card diff-card";

    const stats = c.diff && c.diff.stats ? c.diff.stats : {};
    const lines = c.diff && c.diff.lines ? c.diff.lines : [];

    const statsBar =
        "<div class=\"diff-stats\">" +
            "<span class=\"diff-stat added\">+" + escapeHtml(String(stats.added || 0)) + " added</span>" +
            "<span class=\"diff-stat removed\">-" + escapeHtml(String(stats.removed || 0)) + " removed</span>" +
            "<span class=\"diff-stat unchanged\">" + escapeHtml(String(stats.unchanged || 0)) + " unchanged</span>" +
        "</div>";

    const rows = lines.map(function(line) {
        const leftClass = (line.kind === "removed" || line.kind === "changed") ? "diff-cell-removed" : "diff-cell";
        const rightClass = (line.kind === "added" || line.kind === "changed") ? "diff-cell-added" : "diff-cell";

        const leftNum = line.left_num != null ? line.left_num : "";
        const rightNum = line.right_num != null ? line.right_num : "";

        return "<tr>" +
            "<td class=\"diff-num\">" + escapeHtml(String(leftNum)) + "</td>" +
            "<td class=\"" + leftClass + "\"><pre>" + escapeHtml(line.left_text || "") + "</pre></td>" +
            "<td class=\"diff-num\">" + escapeHtml(String(rightNum)) + "</td>" +
            "<td class=\"" + rightClass + "\"><pre>" + escapeHtml(line.right_text || "") + "</pre></td>" +
            "</tr>";
    }).join("");

    el.innerHTML =
        "<h3>" + escapeHtml(c.title) + "</h3>" +
        statsBar +
        "<div class=\"diff-header\">" +
            "<div class=\"diff-header-side\">Original</div>" +
            "<div class=\"diff-header-side\">Refactored</div>" +
        "</div>" +
        "<div class=\"diff-table-wrap\">" +
            "<table class=\"diff-table\"><tbody>" + rows + "</tbody></table>" +
        "</div>";

    container.appendChild(el);
}


function renderUnknown(c, container) {
    const el = document.createElement("div");
    el.className = "card";
    el.innerHTML = "<h3>Unknown Component</h3><pre>" + escapeHtml(JSON.stringify(c, null, 2)) + "</pre>";
    container.appendChild(el);
}


function escapeHtml(str) {
    return String(str)
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;");
}

window.addEventListener(
    "load",
    loadHistory
);