import React, { useEffect, useRef } from 'react';
import * as THREE from 'three';

export default function HeroNetworkSphere() {
  const mountRef = useRef(null);

  useEffect(() => {
    if (!mountRef.current) return;

    const container = mountRef.current;
    const width = container.clientWidth || 400;
    const height = container.clientHeight || 320;

    let renderer;
    try {
      renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true, powerPreference: "high-performance" });
    } catch (e) {
      console.warn("WebGL not supported");
      return;
    }

    renderer.setSize(width, height);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    container.appendChild(renderer.domElement);

    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(50, width / height, 0.1, 1000);
    camera.position.z = 4.5;

    // Centerpiece 3D Network Globe & Nodes
    const mainGroup = new THREE.Group();
    scene.add(mainGroup);

    // 1. Outer Wireframe Globe Grid
    const outerGeo = new THREE.IcosahedronGeometry(2.0, 3);
    const outerMat = new THREE.MeshBasicMaterial({
      color: 0x2563eb,
      wireframe: true,
      transparent: true,
      opacity: 0.25
    });
    const outerMesh = new THREE.Mesh(outerGeo, outerMat);
    mainGroup.add(outerMesh);

    // 2. Risk Signal Nodes (Real Signal Representations)
    const nodeCount = 45;
    const nodePositions = [];
    const nodeColors = [];
    const nodeGroup = new THREE.Group();
    mainGroup.add(nodeGroup);

    const nodeGeo = new THREE.SphereGeometry(0.06, 12, 12);

    for (let i = 0; i < nodeCount; i++) {
      const u = Math.random();
      const v = Math.random();
      const theta = u * 2.0 * Math.PI;
      const phi = Math.acos(2.0 * v - 1.0);
      const r = 2.02;

      const x = r * Math.sin(phi) * Math.cos(theta);
      const y = r * Math.sin(phi) * Math.sin(theta);
      const z = r * Math.cos(phi);
      nodePositions.push(new THREE.Vector3(x, y, z));

      const rand = Math.random();
      let nodeColor = 0x3b82f6; // Blue
      if (rand > 0.85) nodeColor = 0xef4444; // Critical Red
      else if (rand > 0.65) nodeColor = 0xf59e0b; // Amber

      const mat = new THREE.MeshBasicMaterial({ color: nodeColor });
      const mesh = new THREE.Mesh(nodeGeo, mat);
      mesh.position.set(x, y, z);
      nodeGroup.add(mesh);
    }

    // 3. Connecting Network Lines between Signal Nodes
    const lineMat = new THREE.LineBasicMaterial({
      color: 0x3b82f6,
      transparent: true,
      opacity: 0.35
    });

    const linesGeo = new THREE.BufferGeometry();
    const linePositions = [];

    for (let i = 0; i < nodePositions.length; i++) {
      for (let j = i + 1; j < nodePositions.length; j++) {
        const dist = nodePositions[i].distanceTo(nodePositions[j]);
        if (dist < 1.3) {
          linePositions.push(nodePositions[i].x, nodePositions[i].y, nodePositions[i].z);
          linePositions.push(nodePositions[j].x, nodePositions[j].y, nodePositions[j].z);
        }
      }
    }

    linesGeo.setAttribute('position', new THREE.Float32BufferAttribute(linePositions, 3));
    const linesMesh = new THREE.LineSegments(linesGeo, lineMat);
    mainGroup.add(linesMesh);

    // 4. Inner Glowing AI Core
    const innerGeo = new THREE.SphereGeometry(1.2, 24, 24);
    const innerMat = new THREE.MeshBasicMaterial({
      color: 0x1d4ed8,
      transparent: true,
      opacity: 0.2
    });
    const innerMesh = new THREE.Mesh(innerGeo, innerMat);
    mainGroup.add(innerMesh);

    // 60FPS Smooth Animation Loop
    let animId;
    const animate = () => {
      animId = requestAnimationFrame(animate);
      mainGroup.rotation.y += 0.003;
      mainGroup.rotation.x += 0.0015;
      renderer.render(scene, camera);
    };

    animate();

    const handleResize = () => {
      if (!container) return;
      const w = container.clientWidth || 400;
      const h = container.clientHeight || 320;
      camera.aspect = w / h;
      camera.updateProjectionMatrix();
      renderer.setSize(w, h);
    };

    window.addEventListener('resize', handleResize);

    return () => {
      cancelAnimationFrame(animId);
      window.removeEventListener('resize', handleResize);
      if (mountRef.current && renderer.domElement) {
        mountRef.current.removeChild(renderer.domElement);
      }
      outerGeo.dispose();
      outerMat.dispose();
      nodeGeo.dispose();
      lineMat.dispose();
      linesGeo.dispose();
      innerGeo.dispose();
      innerMat.dispose();
      renderer.dispose();
    };
  }, []);

  return (
    <div className="relative w-full h-[320px] flex items-center justify-center">
      <div ref={mountRef} className="w-full h-full" />
      <div className="absolute bottom-3 right-3 text-[11px] font-bold text-blue-400 bg-slate-950/90 px-3 py-1 rounded-lg border border-blue-500/40 backdrop-blur shadow-lg flex items-center gap-2">
        <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
        AI RISK INTELLIGENCE GRID
      </div>
    </div>
  );
}
