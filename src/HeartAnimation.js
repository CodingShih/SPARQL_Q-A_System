// HeartAnimation.js
import React from 'react';
import { motion } from 'framer-motion';

function HeartAnimation() {
  const [hearts, setHearts] = React.useState([]);

  const handleClick = (e) => {
    const newHeart = {
      x: e.clientX,
      y: e.clientY,
      id: Date.now(),
    };
    setHearts([...hearts, newHeart]);
  };

  return (
    <div onClick={handleClick} style={{ position: 'relative' }}>
      {hearts.map((heart) => (
        <motion.div
          key={heart.id}
          initial={{ opacity: 1, scale: 1 }}
          animate={{ opacity: 0, scale: 2 }}
          transition={{ duration: 1 }}
          style={{
            position: 'absolute',
            top: heart.y,
            left: heart.x,
            width: 20,
            height: 20,
            background: 'red',
            clipPath: 'path("M10 30 A20 20 0 1 1 30 10 A20 20 0 1 1 10 30")',
          }}
        />
      ))}
    </div>
  );
}

export default HeartAnimation;
