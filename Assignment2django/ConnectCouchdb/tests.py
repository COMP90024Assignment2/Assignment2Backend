import React, { useState } from "react";
import "./App.css"; // 导入样式表
import * as d3 from "d3";

function App() {
  const [data, setData] = useState([]);

  const handleClick = async (buttonNumber) => {
    const response = await fetch(`http://your-django-api.com/data/${buttonNumber}`);
    const json = await response.json();
    setData(json);
  };

  return (
    <div className="container">
      <div className="row">
        <button className="button" onClick={() => handleClick(1)}>按钮1</button>
        <button className="button" onClick={() => handleClick(2)}>按钮2</button>
        <button className="button" onClick={() => handleClick(3)}>按钮3</button>
      </div>
      <div className="row">
        <button className="button" onClick={() => handleClick(4)}>按钮4</button>
        <button className="button" onClick={() => handleClick(5)}>按钮5</button>
        <button className="button" onClick={() => handleClick(6)}>按钮6</button>
      </div>
      <div className="row">
        {data.map((d, i) => (
          <div key={i} className="bar" style={{ height: `${d.value}px` }}></div>
        ))}
      </div>
    </div>
  );
}

export default App;