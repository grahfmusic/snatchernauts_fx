# example_scene.rpy — How to use the Snatchernauts FX Plugin in a scene

# This file can live anywhere under game/, e.g. game/example_scene.rpy

label start:
    "Welcome to Snatchernauts FX demo."

    # Rebind our hotkeys to avoid conflicts (optional)
    $ snfx.keys.bind(open_editor="K_F6", toggle_hud="K_F7", prev="K_a", next="K_d")
    $ snfx.debug(True)

    "Open the editor with F6 (we just rebound it)."
    $ snfx.open_editor()

    "When the editor is open, gameplay is paused. Closing it resumes."

    # Load a look:
    $ snfx.lb.load("Scope_Calm")
    $ snfx.lb.speed("fast")
    $ snfx.lb.show(True)

    $ snfx.crt.load("CRT_Arcade")
    $ snfx.grain.load("Cinema_35mm_Soft")
    $ snfx.bloom.load("Bloom_Cinematic")
    $ snfx.grade.load("Teal_Orange")

    # Sample lighting scene
    $ snfx.lights.clear()
    $ snfx.lights.set_ambient(0.12,0.12,0.15, 0.55)
    $ L = snfx.lights.add_point(0.5, 0.6, color=(1.0,0.9,0.7), intensity=1.15, radius=0.35, falloff=1.1, front=False)
    $ snfx.lights.set_anim(L, type="flicker", speed=1.6, amount=0.2)

    "Lights + Bloom combine for a cinematic glow."

    menu:
        "What next?":
            "Preview different CRTs":
                $ snfx.crt.load("CRT_ScanSweep")
                "Scan sweep look applied."
            "Preview different Bloom":
                $ snfx.bloom.load("Bloom_Neon")
                "Neon bloom applied."
            "Open the Editor again":
                $ snfx.open_editor()
                "Back from the editor."

    "Toggle HUD with F7 (as rebound)."
    "You can disable hotkeys entirely if you integrate your own UI."
    $ snfx.keys.enable(False)
    "Hotkeys disabled. Re-enable later with snfx.keys.enable(True)."

    "End of demo."
    return
