function JsonInspector({ data }) {
  return (
    <div className="inspector-card">

      <h2>A2UI Payload Inspector</h2>

      <pre>
        {
          JSON.stringify(
            data,
            null,
            2
          )
        }
      </pre>

    </div>
  );
}

export default JsonInspector;