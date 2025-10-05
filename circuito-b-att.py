import sympy as sp
import numpy as np
import control as ct
import matplotlib.pyplot as plt
from scipy import signal


# Definição dos valores dos componentes
r1, r2 = 100, 150
l1, l2 = 10e-3, 15e-3
c1 = 100e-9

# Setando para Lei dos Nós
s, R1, R2, L1, L2, C = sp.symbols('s R1 R2 L1 L2 C')
Vi, Vb, Vo = sp.symbols('Vi Vb Vo')

# Equações de Nó 
#i1=i4+i3 -> -i1+i4+i3=0 -> literalmente troca as posicoes do Vi-Vb/Ls para Vb-Vi/Ls
eq1 = sp.Eq(((Vb - Vi) / (s * L1)) + (Vb / R1) + ((Vb - Vo) / R2), 0)
#i4 = i0+i5 -> i0-i4+i5
eq2 = sp.Eq(((Vo - Vi) * s * C) + ((Vo - Vb) / R2) + (Vo / (s * L2)), 0)
solucao = sp.solve([eq1, eq2], [Vb, Vo])
H_s_symbolic = sp.simplify(solucao[Vo] / Vi)
sp.pretty_print(H_s_symbolic)

#H(s) Fc de transferencia substituindo valor

num, den = sp.fraction(H_s_symbolic)
num_poly = sp.poly(num, s)
den_poly = sp.poly(den, s)
num_sub_expr = num_poly.subs({R1: r1, R2: r2, L1: l1, L2: l2, C: c1})
den_sub_expr = den_poly.subs({R1: r1, R2: r2, L1: l1, L2: l2, C: c1})
num_final_poly = sp.poly(num_sub_expr, s)
den_final_poly = sp.poly(den_sub_expr, s)
num_coeffs = [float(c) for c in num_final_poly.all_coeffs()]
den_coeffs = [float(c) for c in den_final_poly.all_coeffs()]
H = ct.tf(num_coeffs, den_coeffs)
print("\n\n--- Função de Transferência Numérica H(s) ---")
print(H)


# Mapa de zeros e polos

print("\n--- (ii) Mapa de Polos e Zeros ---")
polos = H.poles()
zeros = H.zeros()
print("\nPolos do sistema:", polos)
print("Zeros do sistema:", zeros)

plt.figure(figsize=(8, 8))
ct.pzmap(H, title='(ii) Diagrama de Polos e Zeros')
plt.savefig('ii_diagrama_polos_zeros.png')
print("\nGráfico salvo em: 'ii_diagrama_polos_zeros.png'")

#3-fracoes parciais
print("\n--- (iii) Componentes da Inversa de Laplace (Frações Parciais) ---")


residos, poles, k = signal.residue(num_coeffs, den_coeffs)
print("\nResíduos (R):", residos)
print("Polos (P):", poles)
print("Termo Direto (k):", k)


t = np.linspace(0, 0.015, 1500)

plt.figure(figsize=(12, 8))
plt.title('(iii) Componentes da Transformada Inversa de Laplace')
plt.xlabel('Tempo (s)')
plt.ylabel('Amplitude')
plt.grid(True)

# Itera sobre os polos e resíduos para plotar cada componente
processar_polos = []
for i in range(len(poles)):
    if poles[i] in processar_polos:
        continue

    # Verifica se o polo é complexo para tratar o par conjugado
    if np.iscomplex(poles[i]):
        conjugado = np.conj(poles[i])
        j = np.where(np.isclose(poles, conjugado))[0][0]
        
        p1 = poles[i]
        r1 = residos[i]
        p2 = poles[j]
        r2 = residos[j]
        
        componente = r1 * np.exp(p1 * t) + r2 * np.exp(p2 * t)
        plt.plot(t, componente.real, label=f'Componente do par de polos em {-p1.real:.2f} ± {p1.imag:.2f}j')
        
        processar_polos.append(p1)
        processar_polos.append(p2)
    else:
        # Se o polo for real
        p = poles[i]
        r = residos[i]
        componente = r * np.exp(p * t)
        plt.plot(t, componente.real, label=f'Componente do polo em {p.real:.2f}', linestyle='--')
        processar_polos.append(p)

plt.legend()
plt.savefig('iii_componentes_inversa_laplace.png')
print("\nGráfico salvo em: 'iii_componentes_inversa_laplace.png'")

#Impulso / Delta de Dirac
print("\n--- (iv) Resposta ao Impulso ---")
plt.figure(figsize=(12, 8))
T_imp, yout_imp = ct.impulse_response(H, T=t)
plt.plot(T_imp, yout_imp)
plt.title('(iv) Resposta ao Impulso Unitário')
plt.xlabel('Tempo (s)')
plt.ylabel('Amplitude Vo(t)')
plt.grid(True)
plt.savefig('iv_resposta_impulso.png')
print("Gráfico salvo em: 'iv_resposta_impulso.png'")

# Degrau unitario
print("\n--- (v) Resposta ao Degrau Unitário ---")
plt.figure(figsize=(12, 8))
T_step, yout_step = ct.step_response(H, T=t)
plt.plot(T_step, yout_step)
plt.title('(v) Resposta ao Degrau Unitário')
plt.xlabel('Tempo (s)')
plt.ylabel('Amplitude Vo(t)')
plt.grid(True)
plt.savefig('v_resposta_degrau.png')
print("Gráfico salvo em: 'v_resposta_degrau.png'")

print("\n\nAs imagens dos gráficos foram salvas na mesma pasta.")
