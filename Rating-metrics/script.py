import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.datasets import make_classification
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix

def calcular_metricas(vp, vn, fp, fn):
    acuracia = (vp + vn) / (vp + vn + fp + fn)
    precisao = vp / (vp + fp) if (vp + fp) > 0 else 0
    sensibilidade = vp / (vp + fn) if (vp + fn) > 0 else 0
    especificidade = vn / (vn + fp) if (vn + fp) > 0 else 0
    fscore = 2 * (precisao * sensibilidade) / (precisao + sensibilidade) if (precisao + sensibilidade) > 0 else 0
    return acuracia, precisao, sensibilidade, especificidade, fscore

X, y = make_classification(n_samples=1000, n_features=10, n_classes=2, random_state=42)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

modelo = RandomForestClassifier(random_state=42)
modelo.fit(X_train, y_train)
y_pred = modelo.predict(X_test)

matriz = confusion_matrix(y_test, y_pred)
vp, fn, fp, vn = matriz.ravel()

acuracia, precisao, sensibilidade, especificidade, fscore = calcular_metricas(vp, vn, fp, fn)

print("Matriz de Confusão:")
print(matriz)
print();
print(f"Acurácia: {acuracia:.2f}")
print(f"Precisão: {precisao:.2f}")
print(f"Sensibilidade (Recall): {sensibilidade:.2f}")
print(f"Especificidade: {especificidade:.2f}")
print(f"F1-Score: {fscore:.2f}")

fig, ax = plt.subplots(1, 2, figsize=(12, 5))

cax = ax[0].matshow(matriz, cmap=plt.cm.Blues, alpha=0.8)
fig.colorbar(cax, ax=ax[0])
for (i, j), val in np.ndenumerate(matriz):
    ax[0].text(j, i, f'{val}', ha='center', va='center', color='black')
ax[0].set_title('Matriz de Confusão')
ax[0].set_xlabel('Previsto')
ax[0].set_ylabel('Verdadeiro')

metricas = ['Acurácia', 'Precisão', 'Sensibilidade', 'Especificidade', 'F1-Score']
valores = [acuracia, precisao, sensibilidade, especificidade, fscore]
ax[1].bar(metricas, valores, color='skyblue')
ax[1].set_ylim(0, 1)
ax[1].set_title('Métricas de Avaliação')
ax[1].set_ylabel('Valor')

plt.tight_layout()
plt.show()
