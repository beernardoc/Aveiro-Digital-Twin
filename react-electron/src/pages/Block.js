import './Block.css';

export default function Block() {

  const blockRoundabout = () => {
    window.location.href = '/block-roundabout';
  }
  
  return (
    <div className="block-page-container">
        <div className="block-page">
            <h1 style={{color: "black", fontSize: "40px", paddingBottom: "30px"}}>Block a Road Segment</h1>
            
            <div className="block-page-buttons">
                {/* 2 buttons, one to block roundabout and another to road */}
                <button className="block-page-button" type='submit' onClick={blockRoundabout} style={{ marginRight: "30px" }}>Block Roundabout</button>
                <button className="block-page-button" type='submit'>Block Road</button>
            </div>

            <div className="block-page-blocks" style={{ marginTop: "30px" }}>
                <div className="block-page-block">
                    <h3 style={{color: "black", fontSize: "20px", paddingBottom: "10px"}}>Active Blocks</h3>
                    <div className="">
                        <h4>BLOCK CARDS</h4>
                    </div>
                </div>
            </div>
        </div>
    </div>
  );
}