<template>
    <div>
      <h1>Koka sijas nestspējas aprēķins</h1>
      <label>Garums, L (m): <input v-model.number="L" /></label>
      <label>Platums, B (m): <input v-model.number="B" /></label>
      <label>Augstums, H (m): <input v-model.number="H" /></label>
      <label>Stiprība, f (KPa): <input v-model.number="f" /></label>
      <button @click="calculate">Aprēķināt</button>
      <p v-if="result !== null">Rezultāts (q): {{ result.toFixed(2) }} kN/m</p>
      <div id="3d-canvas"></div>
    </div>
  </template>
  
  <script>
  import * as THREE from 'three'
  
  export default {
    data() {
      return {
        L: 6,
        B: 0.1,
        H: 0.3,
        f: 20000,
        result: null
      }
    },
    mounted() {
      this.create3D()
    },
    methods: {
      calculate() {
        fetch('http://localhost:5000/api/calculate', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ L: this.L, B: this.B, H: this.H, f: this.f })
        })
          .then(res => res.json())
          .then(data => {
            this.result = data.q
            this.update3D()
          })
      },
      create3D() {
        this.scene = new THREE.Scene()
        this.camera = new THREE.PerspectiveCamera(75, 1, 0.1, 1000)
        this.renderer = new THREE.WebGLRenderer()
        this.renderer.setSize(400, 400)
        document.getElementById('3d-canvas').appendChild(this.renderer.domElement)
        this.geometry = new THREE.BoxGeometry(this.L, this.H, this.B)
        this.material = new THREE.MeshBasicMaterial({ color: 0x00ff00 })
        this.cube = new THREE.Mesh(this.geometry, this.material)
        this.scene.add(this.cube)
        this.camera.position.z = 5
        this.animate()
      },
      update3D() {
        this.scene.remove(this.cube)
        this.geometry = new THREE.BoxGeometry(this.L, this.H, this.B)
        this.cube = new THREE.Mesh(this.geometry, this.material)
        this.scene.add(this.cube)
      },
      animate() {
        requestAnimationFrame(this.animate)
        this.renderer.render(this.scene, this.camera)
      }
    }
  }
  </script>
  
  <style>
  #3d-canvas { margin-top: 20px; }
  </style>
  
