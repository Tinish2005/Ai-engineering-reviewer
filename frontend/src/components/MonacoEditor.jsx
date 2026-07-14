import Editor from "@monaco-editor/react";

function MonacoEditor({
  value,
  onChange,
}) {
  return (
    <div className="editor-card">
      <Editor
        height="500px"
        defaultLanguage="python"
        theme="vs-dark"
        value={value}
        onChange={(value) =>
          onChange(value || "")
        }
      />
    </div>
  );
}

export default MonacoEditor;