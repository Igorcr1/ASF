import sympy as sp
import numpy as np
import control as ct
import matplotlib.pyplot as plt
from scipy import signal


#def componentes
r1, r2 = 100, 150
l1, l2 = 10e-3, 15e-3
c1 = 100e-9

#set lei dos nos
s, G1, G2, L1, L2, C = sp.symbols('s G1 G2 L1 L2 C')
Vi, Vb, Vo = sp.symbols('Vi Vb Vo')

#equacoes 1 e 2 para as lei dos nos 
eq1 = sp.Eq(((Vi - Vb) / (s * L1)) - (Vb * G1) - ((Vb-Vo)*G2), 0)
eq2 = sp.Eq((-(Vo-Vi) * s * C) + ((Vb - Vo) * G2) - (Vo / (s * L2)), 0)
solucao = sp.solve([eq1, eq2], [Vb, Vo])
H_s_symbolic = sp.simplify(solucao[Vo] / Vi)
sp.pretty_print(H_s_symbolic)

#H(s) Fc de transferencia substituindo valor

num, den = sp.fraction(H_s_symbolic)
num_poly = sp.poly(num, s)
den_poly = sp.poly(den, s)
num_sub_expr = num_poly.subs({G1: 1/r1, G2: 1/r2, L1: l1, L2: l2, C: c1})
den_sub_expr = den_poly.subs({G1: 1/r1, G2: 1/r2, L1: l1, L2: l2, C: c1})
num_final_poly = sp.poly(num_sub_expr, s)
den_final_poly = sp.poly(den_sub_expr, s)
num_coeffs = [float(c) for c in num_final_poly.all_coeffs()]
den_coeffs = [float(c) for c in den_final_poly.all_coeffs()]
H = ct.tf(num_coeffs, den_coeffs)
print("\n\n--- Função de Transferência Numérica H(s) ---")
print(H)

zeros = ct.zeros(H)
polos = ct.poles(H)

print("\n\n--- Zeros do Sistema ---")
print(zeros)

print("\n\n--- Polos do Sistema ---")
print(polos)

R, P, K = signal.residue(num_coeffs, den_coeffs)

print("\n\n--- Expansão em Frações Parciais ---")
print("Resíduos (R):")
print(R)
print("\nPolos correspondentes (P):")
print(P)

print("\nDecomposição H(s):")
for i in range(len(R)):
    print(f"  ({R[i]:.4f}) / (s - ({P[i]:.4f}))")
    if i < len(R) - 1:
        print("  +")

#2Parte
t = np.linspace(0, 0.001, 3000)

#curvas da componente de Laplace inversa
fig1 = plt.figure(1)
plt.title('Componentes da Resposta no Tempo (Frações Parciais)')
plt.suptitle('iii. Curvas das Componentes da Transformada Inversa', fontsize=16)

#Polos e residuos
num_coeffs_sci = H.num[0][0]
den_coeffs_sci = H.den[0][0]

#np.exp para as componentes
for i in range(len(R)):
    componente_t = R[i] * np.exp(P[i] * t)
    plt.plot(t, np.real(componente_t), label=f'Componente do polo P={P[i]:.2f}')

plt.xlabel('Tempo (s)')
plt.ylabel('Amplitude')
plt.grid(True)
plt.legend()
# Salva a figura 1
plt.savefig('componentes_resposta_parcial.png')
print("\nImagem 'componentes_resposta_parcial.png' salva.")


#plotando o impulso de dirac
fig2 = plt.figure(2)
t_imp, y_imp = ct.impulse_response(H, T=t)
plt.plot(t_imp, y_imp)
plt.title('Resposta ao Impulso Unitário')
plt.suptitle('iv. Resposta ao Impulso Delta de Dirac', fontsize=16)
plt.xlabel('Tempo (s)')
plt.ylabel('Amplitude Vo(t)')
plt.grid(True)
# Salva a figura 2
plt.savefig('resposta_impulso.png')
print("Imagem 'resposta_impulso.png' salva.")


#degrau unitario
fig3 = plt.figure(3)
t_step, y_step = ct.step_response(H, T=t)
plt.plot(t_step, y_step)
plt.title('Resposta ao Degrau Unitário')
plt.suptitle('v. Resposta ao Degrau Unitário', fontsize=16)
plt.xlabel('Tempo (s)')
plt.ylabel('Amplitude Vo(t)')
plt.grid(True)
# Salva a figura 3
plt.savefig('resposta_degrau.png')
print("Imagem 'resposta_degrau.png' salva.")
plt.close('all')

print("\nAs 3 imagens foram salvas na pasta.")
