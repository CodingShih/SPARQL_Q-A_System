// src/components/Home.js
import React, { useEffect, useMemo, useState } from 'react';
import Particles, { initParticlesEngine } from "@tsparticles/react";
import { loadSlim } from "@tsparticles/slim";

const Home = () => {
  const [init, setInit] = useState(false);

  // Initialize tsparticles engine
  useEffect(() => {
    initParticlesEngine(async (engine) => {
      await loadSlim(engine);
    }).then(() => {
      setInit(true);
    }); 
  }, []);

  const particlesLoaded = (container) => {
    console.log('Particles Loaded:', container);
  };

  const options = useMemo(() => ({
    background: {
      color: { value: "#272829" }, // Set the background color
    },
    fpsLimit: 120,
    interactivity: {
      events: {
        onClick: { enable: true, mode: "push" },
        onHover: { enable: true, mode: "repulse" },
      },
      modes: {
        push: { quantity: 4 },
        repulse: { distance: 200, duration: 0.4 },
      },
    },
    particles: {
      color: { value: "#d6a742" },
      links: {
        color: "#ffffff",
        distance: 150,
        enable: true,
        opacity: 0.5,
        width: 1,
      },
      move: {
        enable: true,
        speed: 6,
        outModes: { default: "bounce" },
      },
      number: {
        density: { enable: true },
        value: 80,
      },
      opacity: { value: 0.5 },
      shape: { type: "circle" },
      size: { value: { min: 1, max: 5 } },
    },
    detectRetina: true,
  }), []);

  if (!init) {
    return null; // Render nothing or a loader until particles are initialized
  }

  return (
    <div className="home-container">
      <Particles
        id="tsparticles"
        options={options}
        particlesLoaded={particlesLoaded}
        className="particles-container"
      />
      <div className="home-content">
        <h1>這裡是JasonIT x Finance 的小天地</h1>
        <p>歡迎到處參觀!</p>
      </div>
    </div>
  );
};

export default Home;
