from flask import Flask, render_template, request, redirect
import os

app = Flask(__name__)

# =========================
# DADOS EM MEMÓRIA
# =========================
lancamentos = []
total_bruto = 0
total_taxas = 0
total_descontos = 0  # protético
total_liquido = 0


# =========================
# ROTA PRINCIPAL
# =========================
@app.route("/", methods=["GET", "POST"])
def index():
    global total_bruto, total_taxas, total_descontos, total_liquido

    if request.method == "POST":
        try:
            valor = float(request.form["valor"])
            pagamento = request.form["pagamento"]
            desconto_protetico = float(request.form.get("desconto", 0))

            # REGRA TAXA
            if pagamento == "Dinheiro":
                taxa = 0
                valor_pos_taxa = valor
            else:
                taxa = valor * 0.10
                valor_pos_taxa = valor - taxa

            # 🔥 REGRA CORRETA DO PROTÉTICO
            valor_base = valor_pos_taxa - desconto_protetico

            # divisão correta
            rayssa = valor_base / 2
            luana = (valor_base / 2) + desconto_protetico

            # salva lançamento
            lancamentos.append({
                "valor_original": valor,
                "pagamento": pagamento,
                "taxa": taxa,
                "valor_pos_taxa": valor_pos_taxa,
                "desconto_protetico": desconto_protetico,
                "valor_base": valor_base,
                "rayssa": rayssa,
                "luana": luana
            })

            # acumula totais
            total_bruto += valor
            total_taxas += taxa
            total_descontos += desconto_protetico
            total_liquido += valor_pos_taxa

        except Exception as e:
            print("Erro:", e)

        return redirect("/")

    # =========================
    # CÁLCULO FINAL
    # =========================
    total_base = total_liquido - total_descontos

    total_rayssa = total_base / 2
    total_luana = (total_base / 2) + total_descontos

    return render_template(
        "index.html",
        lancamentos=lancamentos,
        total_bruto=total_bruto,
        total_taxas=total_taxas,
        total_descontos=total_descontos,
        total_liquido=total_liquido,
        total_rayssa=total_rayssa,
        total_luana=total_luana
    )


# =========================
# LIMPAR DIA
# =========================
@app.route("/limpar")
def limpar():
    global lancamentos, total_bruto, total_taxas, total_descontos, total_liquido

    lancamentos = []
    total_bruto = 0
    total_taxas = 0
    total_descontos = 0
    total_liquido = 0

    return redirect("/")


# =========================
# RODAR LOCAL / SERVIDOR
# =========================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))
    app.run(host="0.0.0.0", port=port)