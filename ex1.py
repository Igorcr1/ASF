import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
import os


output_dir = "analise_massa_mola"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

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
sp.pprint(H_s, use_unicode=True)
print("\n\nFunção inversa da transformada de laplace para o Delta de Dirac:")
sp.pprint(h_t, use_unicode=True)
print("\n\nInversa da Transformada para o degrau unitário:")
sp.pprint(y_t, use_unicode=True)
print("--------------------------\n")


print("\n--- Análise de Polos e Zeros ---")
#extrai os coeficientes do numerador e denominador
numerador_coeffs = [float(c) for c in sp.Poly(sp.numer(H_s), s).all_coeffs()]
denominador_coeffs = [float(c) for c in sp.Poly(sp.denom(H_s), s).all_coeffs()]
lti_system = signal.TransferFunction(numerador_coeffs, denominador_coeffs)

#extrai e imprime os polos e zeros
poles = lti_system.poles
zeros = lti_system.zeros
print(f"Polos: {poles}")
print(f"Zeros: {zeros}")

#cria o gráfico do mapa
plt.figure(figsize=(8, 8))
plt.scatter(np.real(poles), np.imag(poles), s=120, marker='x', color='red', label='Polos')
if len(zeros) > 0:
    plt.scatter(np.real(zeros), np.imag(zeros), s=120, marker='o', facecolors='none', edgecolors='blue', linewidths=1.5, label='Zeros')
plt.title('Mapa de Polos e Zeros')
plt.xlabel('Eixo Real (σ)')
plt.ylabel('Eixo Imaginário (jω)')
plt.axhline(0, color='black', lw=0.5)
plt.axvline(0, color='black', lw=0.5)
plt.grid(True)
plt.legend()
plt.axis('equal')

filename_pz = os.path.join(output_dir, 'mapa_polos_zeros.png')
plt.savefig(filename_pz)
plt.close() # Fecha a figura para não interferir nas próximas
print(f"Salvo na pasta: '{filename_pz}'.")


print("\n--- Análise das Componentes das Frações Parciais ---")
H_s_parciais = sp.apart(H_s, s)
print("\nH(s) expandido em frações parciais:")
sp.pprint(H_s_parciais, use_unicode=True)

#prepara para plotagem
t_vals = np.linspace(0, 50, 500)
plt.figure(figsize=(10, 6))
h_t_total_check = np.zeros_like(t_vals, dtype=complex)


for termo in H_s_parciais.as_ordered_terms():
    h_t_comp_sym = sp.inverse_laplace_transform(termo, s, t)
    h_t_comp_func = sp.lambdify(t, h_t_comp_sym, 'numpy')
    h_t_comp_vals = h_t_comp_func(t_vals)
    h_t_total_check += h_t_comp_vals
    plt.plot(t_vals, np.real(h_t_comp_vals), label=f'Componente de $\\mathcal{{L}}^{{-1}}${{{sp.latex(termo)}}}')


plt.plot(t_vals, np.real(h_t_total_check), 'k--', label='Soma das Componentes (h(t))', linewidth=2)

plt.title('Curvas das Componentes da Transformada Inversa')
plt.xlabel('Tempo (s)')
plt.ylabel('Amplitude')
plt.grid(True)
plt.legend()
plt.ylim(-3, 3) 

filename_comp = os.path.join(output_dir, 'componentes_parciais.png')
plt.savefig(filename_comp)
plt.close()
print(f"Salvo na pasta: '{filename_comp}'.")



print("\n--- Análise das Respostas ao Impulso e Degrau ---")
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
plt.plot(t_vals, np.exp(-zeta * omega_n * t_vals), 'r--', label=r'Envoltória $e^{-\zeta\omega_n t}$', alpha=0.6)
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
#salva o gráfico
filename_orig = os.path.join(output_dir, 'respostas_impulso_degrau.png') 
plt.savefig(filename_orig)
plt.close()
print(f"Salvo na pasta: '{filename_orig}'.")
