import React, { useState } from "react";

function ParametersForm({ params, form, handleChange, updateParams }) {
  const [open, setOpen] = useState(false); // Accordion closed by default
  if (Object.keys(params).length === 0) {
    return <div className="alert alert-danger">No parameters found. Please check backend or config file.</div>;
  }
  // Render parameters in a grid (5 columns per row)
  const entries = Object.entries(params);
  const rows = [];
  for (let i = 0; i < entries.length; i += 5) {
    rows.push(entries.slice(i, i + 5));
  }
  return (
    <div className="accordion" id="paramsAccordion">
      <div className="accordion-item">
        <h2 className="accordion-header" id="paramsHeading">
          <button
            className={`accordion-button${open ? '' : ' collapsed'}`}
            type="button"
            aria-expanded={open}
            aria-controls="paramsCollapse"
            onClick={() => setOpen(o => !o)}
          >
            Parameters
          </button>
        </h2>
        <div
          id="paramsCollapse"
          className={`accordion-collapse collapse${open ? ' show' : ''}`}
          aria-labelledby="paramsHeading"
          data-bs-parent="#paramsAccordion"
        >
          <div className="accordion-body">
            <form className="mb-3">
              <div className="row g-3 w-100">
                {rows.map((row, idx) => (
                  <React.Fragment key={idx}>
                    {row.map(([k, v]) => (
                      <div className="col-12 col-sm-6 col-md-4 col-lg-2" key={k}>
                        <label className="form-label fw-bold" htmlFor={k}>{k}</label>
                        <input
                          className="form-control form-control-sm"
                          id={k}
                          name={k}
                          value={form[k] ?? ''}
                          onChange={handleChange}
                        />
                      </div>
                    ))}
                  </React.Fragment>
                ))}
              </div>
              <button type="button" onClick={updateParams} className="btn btn-primary mt-3">Update Parameters</button>
            </form>
          </div>
        </div>
      </div>
    </div>
  );
}

export default ParametersForm;
