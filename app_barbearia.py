import streamlit as st
import pandas as pd
from datetime import datetime

# Configuração da página
st.set_page_config(page_title="Barbearia do Guilherme", page_icon="💈", layout="centered")

# Inicialização do banco de dados na memória do app
if "agendamentos" not in st.session_state:
    st.session_state.agendamentos = pd.DataFrame(
        columns=["Cliente", "Telefone", "Serviço", "Preço", "Data", "Horário"]
    )

# Dados da barbearia
SERVICOS = {
    "Corte de Cabelo (R$ 40,00)": 40.0,
    "Corte e Barba (R$ 50,00)": 50.0
}
HORARIOS = [f"{h:02d}:00" for h in range(9, 19)]

# Interface do Usuário
st.title("💈 Barbearia do Guilherme")
st.write("Agende seu horário com total facilidade e rapidez!")

aba_cliente, aba_admin = st.tabs(["Agendar Horário", "Painel do Guilherme"])

with aba_cliente:
    st.subheader("Faça seu Agendamento")
    
    with st.form("form_agendamento", clear_on_submit=True):
        nome = st.text_input("Seu Nome:")
        telefone = st.text_input("Seu Celular/WhatsApp:")
        servico_selecionado = st.selectbox("Escolha o Serviço:", list(SERVICOS.keys()))
        data_agendamento = st.date_input("Escolha o Dia:", min_value=datetime.today().date())
        
        # Filtrar horários ocupados
        data_str = str(data_agendamento)
        df_atual = st.session_state.agendamentos
        horarios_ocupados = df_atual[df_atual["Data"] == data_str]["Horário"].tolist()
        horarios_disponiveis = [h for h in HORARIOS if h not in horarios_ocupados]
        
        horario_selecionado = st.selectbox("Escolha o Horário disponível:", horarios_disponiveis if horarios_disponiveis else ["Sem horários livres"])
        
        enviar = st.form_submit_button("Confirmar Agendamento")
        
        if enviar:
            if not nome or not telefone:
                st.error("Por favor, preencha seu nome e telefone.")
            elif horario_selecionado == "Sem horários livres":
                st.error("Não há horários disponíveis para esta data.")
            else:
                preco_servico = SERVICOS[servico_selecionado]
                
                novo_agendamento = {
                    "Cliente": nome,
                    "Telefone": telefone,
                    "Serviço": servico_selecionado,
                    "Preço": preco_servico,
                    "Data": data_str,
                    "Horário": horario_selecionado
                }
                
                st.session_state.agendamentos = pd.concat([st.session_state.agendamentos, pd.DataFrame([novo_agendamento])], ignore_index=True)
                st.success(f"Sucesso, {nome}! Seu horário no dia {data_agendamento.strftime('%d/%m/%Y')} às {horario_selecionado} foi reservado.")
                st.rerun()

with aba_admin:
    st.subheader("Área Restrita do Administrador")
    senha = st.text_input("Digite a senha master para acessar:", type="password")
    
    if senha == "1234":
        st.success("Acesso liberado!")
        df_agendas = st.session_state.agendamentos
        
        if df_agendas.empty:
            st.info("Nenhum agendamento realizado até o momento.")
        else:
            faturamento_total = df_agendas["Preço"].sum()
            total_atendimentos = len(df_agendas)
            
            col1, col2 = st.columns(2)
            col1.metric("Total de Agendamentos", f"{total_atendimentos}")
            col2.metric("Faturamento Estimado", f"R$ {faturamento_total:.2f}")
            
            st.write("### Lista Cronológica de Atendimentos")
            df_ordenado = df_agendas.sort_values(by=["Data", "Horário"])
            st.dataframe(df_ordenado, use_container_width=True)
    elif senha:
        st.error("Senha incorreta.")
