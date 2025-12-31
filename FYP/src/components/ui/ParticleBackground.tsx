import { useEffect, useState } from "react";
import Particles, { initParticlesEngine } from "@tsparticles/react";
import { loadFull } from "tsparticles"; 

interface Props {
  theme: string;
}

const ParticleBackground = ({ theme }: Props) => {
  const [init, setInit] = useState(false);

  // We set 'engine' to 'any' to stop the ts(7006) error
  useEffect(() => {
    initParticlesEngine(async (engine: any) => {
      await loadFull(engine);
    }).then(() => {
      setInit(true);
    });
  }, []);

  // Use 'any' type for options to bypass the namespace ts(2709) error
  const options: any = {
    fullScreen: { enable: true, zIndex: -1 },
    background: {
      color: { value: theme === "light" ? "#FFFFFF" : "#000000" },
    },
    particles: {
      number: { value: 200, density: { enable: true, area: 800 } },
      color: { value: theme === "light" ? "#000000" : "#FFFFFF" },
      shape: { type: "circle" },
      opacity: { value: 0.5 },
      size: { value: { min: 1, max: 3 } },
      links: {
        enable: true,
        distance: 150,
        color: theme === "light" ? "#000000" : "#FFFFFF",
        opacity: 0.3,
        width: 1,
      },
      move: {
        enable: true,
        speed: 1,
        direction: "none",
        outModes: { default: "bounce" },
        attract: {
          enable: true,
          rotate: { x: 600, y: 1200 }
        }
      },
    },
    interactivity: {
      events: {
        onHover: { enable: true, mode: "grab" },
        onClick: { enable: true, mode: "push" },
      },
      modes: {
        grab: { distance: 200, links: { opacity: 0.5 } },
        push: { quantity: 4 },
      },
    },
  };

  if (init) {
    return <Particles id="tsparticles" options={options} />;
  }

  return null;
};

export default ParticleBackground;