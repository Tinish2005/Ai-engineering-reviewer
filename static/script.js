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
            container.innerHTML = "<p class=\"loading-text\">" + escapeHtml(result.message || "Error") + "</p>";
            return;
        }
        renderComponents(result.components, container);
    } catch (err) {
        container.innerHTML = "";
        showLoading(container, "Review failed. Please try again.");
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
        renderCodeCard(component, container);
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
            case "metric_card":     renderMetricCard(c, container); break;
            case "complexity_card": renderComplexityCard(c, container); break;
            case "finding_list":    renderFindingList(c, container); break;
            case "rule_check_card": renderRuleCheckCard(c, container); break;
            case "list":            renderList(c, container); break;
            case "card":            renderSimpleCard(c, container); break;
            case "ai_summary":      renderAISummary(c, container); break;
            case "code_card":       renderCodeCard(c, container); break;
            default:                renderUnknown(c, container); break;
        }
    });
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
