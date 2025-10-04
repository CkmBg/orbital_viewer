// import React from 'react';
import DateSlider from './SliderDate';

const menuStyle = {
    height: '100vh',
    width: '260px',
    background: '#222c3626',
    background: '#222c3626',
    color: '#fff',
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    boxShadow: '2px 0 8px rgba(0,0,0,0.08)',
    zIndex: 1000,
    padding: '1rem',
};

const titleStyle = {
    marginBottom: '40px',
    fontSize: '1.6rem',
    fontWeight: 'bold',
    textAlign: 'center',
    letterSpacing: '1px',
};

function VerticalMenu({loadOrbit, handleTransition, transition}) {
    return (
        <nav style={menuStyle}>
            <div style={titleStyle}>Orbital Visualizer</div>
            <button onClick={loadOrbit} style={{ marginTop: "20px" }}>
                Load Orbit
            </button>
            <div style={{display: 'flex', flexDirection: 'column', alignItems: 'center', marginTop: 'auto', marginBottom: '60px', paddingBottom: '20px', fontSize: '0.9rem', color: '#888',}}>
                <div> BOTTOM NAV </div>
                <div style={{width: '200px', border:'1px solid', display: 'flex', justifyContent: 'space-between', marginTop: '10px'}}>
                    <button onClick={() =>handleTransition(true)}>Dev</button>
                    <div>{transition ? "Zoom in" : "Zoom out"}</div>
                    <button onClick={() =>handleTransition(false)}>Prod</button>
                </div>
            </div>
        </nav>
    );
}

export default VerticalMenu;