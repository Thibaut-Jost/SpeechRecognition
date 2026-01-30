import numpy as np

class FiltersAudio():
    def __init__(self):
        pass

    def highpass_1pole(self, x, fs, fc=120.0):
        # fc = fréquence de coupure (Hz). 80–150 Hz marche bien contre souffle/rumble.
        x = np.asarray(x, dtype=np.float32).flatten()
        alpha = fs / (fs + 2*np.pi*fc)
        y = np.empty_like(x)
        y[0] = x[0]
        for n in range(1, len(x)):
            y[n] = alpha * (y[n-1] + x[n] - x[n-1])
        return y

    def gate_smooth(self,x, fs,
                    open_th=0.020, close_th=0.012,  # hysteresis (close < open)
                    attack_ms=5.0, release_ms=120.0,
                    floor=0.1):
        """
        Noise gate doux:
        - open_th / close_th : seuils sur l'enveloppe (amplitude)
        - attack/release : vitesse d'ouverture/fermeture
        - floor : gain minimum quand c'est "fermé" (0 = mute, 0.1-0.2 conseillé)
        """
        x = np.asarray(x, dtype=np.float32).flatten()

        # Envelope lissée (RMS-ish via abs + lowpass)
        env = np.abs(x)
        # lissage ~10ms
        smooth_ms = 10.0
        a_env = np.exp(-1.0 / (fs * (smooth_ms / 1000.0)))
        env_s = np.empty_like(env)
        env_s[0] = env[0]
        for n in range(1, len(env)):
            env_s[n] = a_env * env_s[n-1] + (1 - a_env) * env[n]

        # Coefs attaque/release (smoothing du gain)
        a_att = np.exp(-1.0 / (fs * (attack_ms / 1000.0)))
        a_rel = np.exp(-1.0 / (fs * (release_ms / 1000.0)))

        y = np.empty_like(x)
        g = 1.0
        state_open = False

        for n in range(len(x)):
            e = env_s[n]

            # hysteresis: on ouvre à open_th, on ferme à close_th
            if state_open:
                if e < close_th:
                    state_open = False
            else:
                if e > open_th:
                    state_open = True

            target = 1.0 if state_open else float(floor)

            # lissage du gain (attaque plus rapide que release)
            if target > g:
                g = a_att * g + (1 - a_att) * target
            else:
                g = a_rel * g + (1 - a_rel) * target

            y[n] = x[n] * g

        return y