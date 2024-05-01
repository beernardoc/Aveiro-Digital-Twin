import './BlockRoundabout.css';
import map from '../asset/map/roundabouts_map.png';
export default function BlockRoundabout() {
    return (
        <div className="roundabout-page-container">
            <div className="roundabout-page">
                <h1 style={{color: "black", fontSize: "40px"}}>Block a Roundabout</h1>
                <h3 style={{color: "black", fontSize: "20px", paddingBottom: "30px"}}>Select the roundabout you want to block</h3>
                <div className="roundabout-page-map">
                    <img src={map} alt="Roundabouts Map" useMap='#roudabout' />

                    <map name="roudabout">
                        <area shape="circle" coords="393,105,10" alt="Roundabout 1" style={{cursor: "pointer"}} id='round_1' onClick={() => alert('Roundabout 1')} />
                        <area shape="circle" coords="551,275,10" alt="Roundabout 2" style={{cursor: "pointer"}} id='round_2' onClick={() => alert('Roundabout 2')} />
                        <area shape="circle" coords="627,611,10" alt="Roundabout 3" style={{cursor: "pointer"}} id='round_3' onClick={() => alert('Roundabout 3')} />
                        <area shape="circle" coords="915,415,10" alt="Roundabout 4" style={{cursor: "pointer"}} id='round_4' onClick={() => alert('Roundabout 4')} />
                    </map> 
                </div>
            </div>
        </div>
    );
}