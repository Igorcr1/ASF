import sympy as sp
import numpy as np
import matplotlib.pyplot as plt

#variaveis e cte's
s, t = sp.symbols('s, t')
m = 1.0  
b = 0.1
k = 0.5

# h(s)
H_s = 1 / (m * s**2 + b * s + k)
h_t = sp.inverse_laplace_transform(H_s, s, t)

# Transformada inversa de Laplace de H(s) * (1/s)
H_degrau = H_s / s
y_t = sp.inverse_laplace_transform(H_degrau, s, t)

#pritando tudo
print("Função de Transfêrencia:")
sp.pprint(H_s)
print("\n\nFunção inversa da transformada de laplace para o Delta de Dirac:")
sp.pprint(h_t)
print("\n\nInversa da Transformada para o degrau unitário:")
sp.pprint(y_t)
print("--------------------------\n")

t_vals = np.linspace(0, 50, 500)

#resposta ao impulso
zeta = b / (2 * np.sqrt(m * k))
omega_n = np.sqrt(k / m) 
omega_d = omega_n * np.sqrt(1 - zeta**2)

h_t_vals = (1 / omega_d) * np.exp(-zeta * omega_n * t_vals) * np.sin(omega_d * t_vals)

y_t_vals = 1 - (np.exp(-zeta * omega_n * t_vals) / np.sqrt(1 - zeta**2)) * np.sin(omega_d * t_vals + np.arccos(zeta))

plt.figure(figsize=(12, 6))

#criando o gráfico
plt.subplot(1, 2, 1)
plt.plot(t_vals, h_t_vals, label=r'Resposta ao Impulso $h(t)$', color='blue')
plt.plot(t_vals, np.exp(-zeta * omega_n * t_vals), 'r--', label=r'$e^{-\zeta\omega_n t}$', alpha=0.6)
plt.plot(t_vals, -np.exp(-zeta * omega_n * t_vals), 'r--', alpha=0.6)
plt.title('Resposta ao Impulso')
plt.xlabel('Tempo (s)')
plt.ylabel('Amplitude')
plt.grid(True)
plt.legend()

#grafico da resp degrau
plt.subplot(1, 2, 2)
plt.plot(t_vals, y_t_vals, label=r'Resposta ao Degrau $y(t)$', color='green')
plt.axhline(1, color='gray', linestyle='--', linewidth=1, label='Valor de estado estacionário')
plt.title('Resposta ao Degrau Unitário')
plt.xlabel('Tempo (s)')
plt.ylabel('Amplitude')
plt.grid(True)
plt.legend()

plt.tight_layout()
plt.savefig('Exercicio1.png') 
print("\nSalvo na pasta: 'Exercicio1.png'.")
