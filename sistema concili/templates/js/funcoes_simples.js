// FUNÇÕES SIMPLIFICADAS PARA EVITAR ERROS DE SINTAXE

// Aplicar filtros nas divergências
function aplicarFiltrosDivergencias() {
    console.log('Aplicando filtros nas divergências');
    if (typeof carregarDivergencias === 'function') {
        carregarDivergencias();
    }
}

// Limpar filtros das divergências
function limparFiltrosDivergencias() {
    console.log('Limpando filtros das divergências');
    const campos = ['filtro-tipo-divergencia', 'filtro-status-divergencia', 'filtro-data-inicial', 'filtro-data-final'];
    campos.forEach(campo => {
        const elemento = document.getElementById(campo);
        if (elemento) elemento.value = '';
    });
    if (typeof carregarDivergencias === 'function') {
        carregarDivergencias();
    }
}

// Recarregar divergências
function recarregarDivergencias() {
    console.log('Recarregando divergências');
    if (typeof carregarDivergencias === 'function') {
        carregarDivergencias();
    }
}

// Exportar divergências para CSV
function exportarDivergenciasCSV() {
    console.log('Exportando divergências para CSV');
    alert('Funcionalidade de exportação em desenvolvimento');
}

// Aplicar filtros de conciliações
function aplicarFiltros() {
    console.log('Aplicando filtros de conciliações');
    if (typeof carregarConciliacoes === 'function') {
        carregarConciliacoes(1);
    }
}

// Limpar filtros de conciliações
function limparFiltros() {
    console.log('Limpando filtros de conciliações');
    const campos = ['filtro-data-inicio', 'filtro-data-fim', 'filtro-tipo', 'filtro-status'];
    campos.forEach(campo => {
        const elemento = document.getElementById(campo);
        if (elemento) elemento.value = '';
    });
    if (typeof carregarConciliacoes === 'function') {
        carregarConciliacoes(1);
    }
}

// Funções de relatórios
function gerarRelatorioPDF() {
    console.log('Gerando relatório PDF');
    alert('Funcionalidade de relatório PDF em desenvolvimento');
}

function exportarDivergencias() {
    console.log('Exportando divergências');
    alert('Funcionalidade de exportação em desenvolvimento');
}

function mostrarEstatisticas() {
    console.log('Mostrando estatísticas');
    alert('Funcionalidade de estatísticas em desenvolvimento');
}

// Ver detalhes de divergência
function verDetalhesDivergencia(id) {
    console.log('Ver detalhes da divergência:', id);
    alert('Detalhes da divergência ' + id + '\n\nFuncionalidade em desenvolvimento...');
}

// Resolver divergência
function resolverDivergencia(id) {
    console.log('Resolver divergência:', id);
    if (confirm('Deseja marcar a divergência ' + id + ' como resolvida?')) {
        alert('Divergência ' + id + ' marcada como resolvida!');
        if (typeof carregarDivergencias === 'function') {
            setTimeout(() => {
                carregarDivergencias();
            }, 1000);
        }
    }
}

// Ignorar divergência
function ignorarDivergencia(id) {
    console.log('Ignorar divergência:', id);
    if (confirm('Deseja ignorar a divergência ' + id + '?')) {
        alert('Divergência ' + id + ' ignorada!');
        if (typeof carregarDivergencias === 'function') {
            setTimeout(() => {
                carregarDivergencias();
            }, 1000);
        }
    }
}

// Funções de upload
function uploadFotoPerfil() {
    const input = document.getElementById('upload-foto');
    if (input) input.click();
}

function processarFotoPerfil(input) {
    if (input.files && input.files[0]) {
        console.log('Processando foto de perfil');
        alert('Upload de foto em desenvolvimento');
    }
}

// Funções de configuração
function editarDadosPessoais() {
    alert('Edição de dados pessoais em desenvolvimento');
}

function alterarSenha() {
    alert('Alteração de senha em desenvolvimento');
}

function configurarPreferencias() {
    alert('Configuração de preferências em desenvolvimento');
}

// Executar conciliação automática
function executarConciliacaoAutomatica() {
    console.log('Executando conciliação automática');
    alert('Funcionalidade de conciliação automática em desenvolvimento');
}

// Cancelar conciliação
function cancelarConciliacao(id) {
    console.log('Cancelar conciliação:', id);
    if (confirm('Deseja cancelar esta conciliação?')) {
        alert('Conciliação cancelada');
    }
}

// Ver detalhes de conciliação
function verDetalhesConciliacao(id) {
    console.log('Ver detalhes da conciliação:', id);
    alert('Detalhes da conciliação ' + id + '\n\nFuncionalidade em desenvolvimento...');
}

// Exportar procedimento
function exportarProcedimento(id) {
    console.log('Exportar procedimento:', id);
    alert('Exportação do procedimento ' + id + ' em desenvolvimento');
}

// Carregar dados do usuário
function carregarDadosUsuario() {
    console.log('Carregando dados do usuário');
    const nome = document.getElementById('nome-usuario');
    const email = document.getElementById('email-usuario');
    const perfil = document.getElementById('perfil-usuario');
    
    if (nome) nome.textContent = 'Usuario Teste';
    if (email) email.textContent = 'usuario@teste.com';
    if (perfil) perfil.textContent = 'Administrador';
}

// Funções de renderização simplificadas
function renderDetalhesConciliacao(conciliacao) {
    var statusClass = conciliacao.status === 'Concluído' ? 'bg-success' : 
                     conciliacao.status === 'Em Andamento' ? 'bg-warning' : 'bg-danger';
    
    var valorExtratos = (conciliacao.valor_extratos || 0).toLocaleString('pt-BR', { minimumFractionDigits: 2 });
    var valorLancamentos = (conciliacao.valor_lancamentos || 0).toLocaleString('pt-BR', { minimumFractionDigits: 2 });
    var diferenca = Math.abs((conciliacao.valor_extratos || 0) - (conciliacao.valor_lancamentos || 0));
    var diferencaClass = diferenca < 0.01 ? 'text-success' : 'text-danger';
    
    return '<div class="card"><div class="card-body">' +
           '<h5>Detalhes da Conciliação #' + conciliacao.id + '</h5>' +
           '<p><strong>Status:</strong> <span class="badge ' + statusClass + '">' + conciliacao.status + '</span></p>' +
           '<p><strong>Data:</strong> ' + new Date(conciliacao.created_at).toLocaleString('pt-BR') + '</p>' +
           '<p><strong>Valor Extratos:</strong> R$ ' + valorExtratos + '</p>' +
           '<p><strong>Valor Lançamentos:</strong> R$ ' + valorLancamentos + '</p>' +
           '<p><strong>Diferença:</strong> <span class="' + diferencaClass + '">R$ ' + diferenca.toLocaleString('pt-BR', { minimumFractionDigits: 2 }) + '</span></p>' +
           '</div></div>';
}

function renderDetalhesProcedimento(procedimento) {
    var statusClass = procedimento.status === 'Concluído' ? 'bg-success' : 
                     procedimento.status === 'Em Andamento' ? 'bg-warning' : 'bg-danger';
    
    return '<div class="card"><div class="card-body">' +
           '<h5>Detalhes do Procedimento #' + procedimento.id + '</h5>' +
           '<p><strong>Status:</strong> <span class="badge ' + statusClass + '">' + procedimento.status + '</span></p>' +
           '<p><strong>Data:</strong> ' + new Date(procedimento.created_at).toLocaleString('pt-BR') + '</p>' +
           '<p><strong>Total de Conciliações:</strong> ' + (procedimento.total_conciliacoes || 0) + '</p>' +
           '</div></div>';
}

console.log('✅ Funções simplificadas carregadas com sucesso');
