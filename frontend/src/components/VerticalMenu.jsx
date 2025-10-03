// import React from 'react';

const menuStyle = {
    height: '100vh',
    width: '260px',
    background: '#222c36',
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

function VerticalMenu({ children }) {
    return (
        <nav style={menuStyle}>
            <div style={titleStyle}>Orbital Visualizer</div>
            {children}
        </nav>
    );
}

export default VerticalMenu;