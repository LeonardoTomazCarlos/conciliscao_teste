// FUNÇÕES SIMPLIFICADAS PARA EVITAR ERROS DE SINTAXE

// Função de debug para verificar persistência de abas
function debugPersistenciaAbas() {
    const abaSalva = localStorage.getItem('abaSistemaAtiva');
    console.log('🔍 Debug - Aba salva no localStorage:', abaSalva);
    return abaSalva;
}

// Função para forçar uma aba específica (para testes)
function forcarAba(nomeAba) {
    localStorage.setItem('abaSistemaAtiva', nomeAba);
    console.log('🔧 Aba forçada para:', nomeAba);
    if (typeof ativarAba === 'function') {
        ativarAba(nomeAba);
    }
}

// Função para limpar persistência (resetar para primeira visita)
function resetarPersistencia() {
    localStorage.removeItem('abaSistemaAtiva');
    console.log('🗑️ Persistência de aba removida - próximo carregamento será Dashboard');
    alert('Persistência removida! Recarregue a página para ver o efeito.');
}

// Função para testar persistência
function testarPersistencia() {
    const abaAtual = localStorage.getItem('abaSistemaAtiva');
    console.log('📋 Teste de persistência:');
    console.log('  - Aba atual salva:', abaAtual);
    console.log('  - Para testar: mude para outra aba e recarregue a página');
    console.log('  - Para resetar: execute resetarPersistencia()');
    console.log('  - Estado das abas visíveis:', Array.from(document.querySelectorAll('.tab-pane.show')).map(t => t.id));
    alert('Aba atual salva: ' + (abaAtual || 'nenhuma') + '\n\nVerifique o console para mais detalhes.');
}

// Função para verificar estado atual das abas
function verificarEstadoAbas() {
    const tabsVisiveis = Array.from(document.querySelectorAll('.tab-pane')).map(tab => {
        return {
            id: tab.id,
            display: tab.style.display,
            classes: tab.className,
            visivel: tab.style.display !== 'none' && tab.classList.contains('show')
        };
    });
    
    console.log('🔍 Estado atual das abas:', tabsVisiveis);
    const abasSalva = localStorage.getItem('abaSistemaAtiva');
    console.log('💾 Aba salva no localStorage:', abasSalva);
    
    return tabsVisiveis;
}

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
    console.log('🔄 Executando conciliação automática...');
    
    // Mostrar indicador de carregamento
    const loadingHtml = `
        <div id="loading-conciliacao" class="position-fixed top-0 start-0 w-100 h-100 d-flex align-items-center justify-content-center" 
             style="background: rgba(0,0,0,0.8); z-index: 9999;">
            <div class="card p-4 text-center">
                <div class="spinner-border text-primary mb-3" role="status"></div>
                <h5>Executando Conciliação Automática</h5>
                <p class="text-muted">Analisando extratos e lançamentos...</p>
            </div>
        </div>
    `;
    document.body.insertAdjacentHTML('beforeend', loadingHtml);
    
    // Fazer requisição para a API
    fetch('/api/conciliacao-automatica', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        credentials: 'same-origin'
    })
    .then(response => response.json())
    .then(data => {
        // Remover loading
        const loading = document.getElementById('loading-conciliacao');
        if (loading) loading.remove();
        
        if (data.success) {
            const mensagem = `✅ CONCILIAÇÃO AUTOMÁTICA CONCLUÍDA\n\n` +
                           `• ${data.conciliados || 0} conciliações realizadas\n` +
                           `• ${data.message || 'Processo concluído com sucesso'}\n\n` +
                           `Os dados foram atualizados automaticamente.`;
            alert(mensagem);
            
            // Recarregar dados da página se necessário
            if (typeof carregarDados === 'function') {
                carregarDados();
            }
        } else {
            alert('❌ Erro na conciliação: ' + (data.error || 'Erro desconhecido'));
        }
    })
    .catch(error => {
        console.error('Erro na conciliação automática:', error);
        
        // Remover loading
        const loading = document.getElementById('loading-conciliacao');
        if (loading) loading.remove();
        
        alert('❌ Erro na conciliação: ' + error.message);
    });
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

// ========================================
// SISTEMA DE FILTROS DE RELATÓRIO
// ========================================

// Aplicar filtros rápidos
function aplicarFiltroRapido(tipo) {
    console.log('⚡ Aplicando filtro rápido:', tipo);
    
    // Limpar filtros primeiro
    limparFiltrosRelatorio();
    
    switch(tipo) {
        case 'hoje':
            document.getElementById('filtro-periodo-relatorio').value = 'hoje';
            break;
            
        case 'semana':
            document.getElementById('filtro-periodo-relatorio').value = '7dias';
            break;
            
        case 'mes':
            document.getElementById('filtro-periodo-relatorio').value = 'mes-atual';
            break;
            
        case 'divergencias':
            document.getElementById('filtro-periodo-relatorio').value = '30dias';
            document.getElementById('filtro-divergencias-relatorio').value = 'com-divergencia';
            break;
    }
    
    // Aplicar filtros automaticamente
    setTimeout(() => {
        aplicarFiltrosRelatorio();
    }, 300);
}

// Aplicar filtros de relatório
function aplicarFiltrosRelatorio() {
    console.log('🔍 Aplicando filtros de relatório...');
    
    const filtros = coletarFiltrosRelatorio();
    console.log('📋 Filtros coletados:', filtros);
    
    // Simular carregamento
    mostrarCarregandoRelatorio(true);
    
    setTimeout(() => {
        // Gerar dados simulados baseados nos filtros
        const dadosSimulados = gerarDadosSimuladosRelatorio(filtros);
        
        // Atualizar estatísticas
        atualizarEstatisticasRelatorio(dadosSimulados.estatisticas);
        
        // Atualizar tabela de preview
        atualizarTabelaPreviewRelatorio(dadosSimulados.registros);
        
        mostrarCarregandoRelatorio(false);
        
        alert('Filtros aplicados com sucesso!\n\n' + 
              'Registros encontrados: ' + dadosSimulados.estatisticas.total + '\n' +
              'Período: ' + filtros.periodo + '\n' +
              'Usuário: ' + (filtros.usuario || 'Todos'));
              
    }, 1500);
}

// Coletar todos os filtros do formulário
function coletarFiltrosRelatorio() {
    return {
        periodo: document.getElementById('filtro-periodo-relatorio').value,
        dataInicio: document.getElementById('filtro-data-inicio-relatorio').value,
        dataFim: document.getElementById('filtro-data-fim-relatorio').value,
        usuario: document.getElementById('filtro-usuario-relatorio').value,
        tipo: document.getElementById('filtro-tipo-relatorio').value,
        status: document.getElementById('filtro-status-relatorio').value,
        valorMin: document.getElementById('filtro-valor-min-relatorio').value,
        valorMax: document.getElementById('filtro-valor-max-relatorio').value,
        divergencias: document.getElementById('filtro-divergencias-relatorio').value,
        arquivo: document.getElementById('filtro-arquivo-relatorio').value
    };
}

// Limpar todos os filtros
function limparFiltrosRelatorio() {
    console.log('🗑️ Limpando filtros de relatório...');
    
    document.getElementById('filtro-periodo-relatorio').value = '30dias';
    document.getElementById('filtro-data-inicio-relatorio').value = '';
    document.getElementById('filtro-data-fim-relatorio').value = '';
    document.getElementById('filtro-usuario-relatorio').value = '';
    document.getElementById('filtro-tipo-relatorio').value = '';
    document.getElementById('filtro-status-relatorio').value = '';
    document.getElementById('filtro-valor-min-relatorio').value = '';
    document.getElementById('filtro-valor-max-relatorio').value = '';
    document.getElementById('filtro-divergencias-relatorio').value = '';
    document.getElementById('filtro-arquivo-relatorio').value = '';
    
    // Esconder campos de data personalizada
    document.getElementById('data-inicio-container').style.display = 'none';
    document.getElementById('data-fim-container').style.display = 'none';
    
    // Limpar resultados
    limparResultadosRelatorio();
    
    alert('Filtros limpos com sucesso!');
}

// Salvar filtros atuais
function salvarFiltrosRelatorio() {
    const filtros = coletarFiltrosRelatorio();
    const nome = prompt('Digite um nome para este conjunto de filtros:');
    
    if (nome) {
        let filtrosSalvos = JSON.parse(localStorage.getItem('filtrosRelatorioSalvos') || '[]');
        
        filtrosSalvos.push({
            nome: nome,
            filtros: filtros,
            dataCriacao: new Date().toISOString()
        });
        
        localStorage.setItem('filtrosRelatorioSalvos', JSON.stringify(filtrosSalvos));
        atualizarListaFiltrosSalvos();
        
        alert('Filtros salvos com sucesso: ' + nome);
    }
}

// Atualizar lista de filtros salvos
function atualizarListaFiltrosSalvos() {
    const filtrosSalvos = JSON.parse(localStorage.getItem('filtrosRelatorioSalvos') || '[]');
    const container = document.getElementById('filtros-salvos-list');
    const containerPrincipal = document.getElementById('filtros-salvos-container');
    
    if (filtrosSalvos.length > 0) {
        containerPrincipal.style.display = 'block';
        
        container.innerHTML = filtrosSalvos.map(item => 
            '<button class="btn btn-sm btn-outline-info me-2 mb-1" onclick="carregarFiltroSalvo(\'' + 
            item.nome + '\')" title="Criado em: ' + new Date(item.dataCriacao).toLocaleString('pt-BR') + '">' +
            '<i class="fas fa-bookmark me-1"></i>' + item.nome +
            '<button class="btn btn-sm btn-link text-danger p-0 ms-2" onclick="removerFiltroSalvo(\'' + 
            item.nome + '\')" title="Remover"><i class="fas fa-times"></i></button>' +
            '</button>'
        ).join('');
    } else {
        containerPrincipal.style.display = 'none';
    }
}

// Carregar filtro salvo
function carregarFiltroSalvo(nome) {
    const filtrosSalvos = JSON.parse(localStorage.getItem('filtrosRelatorioSalvos') || '[]');
    const filtro = filtrosSalvos.find(f => f.nome === nome);
    
    if (filtro) {
        const f = filtro.filtros;
        
        document.getElementById('filtro-periodo-relatorio').value = f.periodo || '30dias';
        document.getElementById('filtro-data-inicio-relatorio').value = f.dataInicio || '';
        document.getElementById('filtro-data-fim-relatorio').value = f.dataFim || '';
        document.getElementById('filtro-usuario-relatorio').value = f.usuario || '';
        document.getElementById('filtro-tipo-relatorio').value = f.tipo || '';
        document.getElementById('filtro-status-relatorio').value = f.status || '';
        document.getElementById('filtro-valor-min-relatorio').value = f.valorMin || '';
        document.getElementById('filtro-valor-max-relatorio').value = f.valorMax || '';
        document.getElementById('filtro-divergencias-relatorio').value = f.divergencias || '';
        document.getElementById('filtro-arquivo-relatorio').value = f.arquivo || '';
        
        // Verificar se precisa mostrar campos de data personalizada
        controlarCamposDataPersonalizada();
        
        alert('Filtros carregados: ' + nome);
    }
}

// Remover filtro salvo
function removerFiltroSalvo(nome) {
    if (confirm('Deseja remover o filtro salvo "' + nome + '"?')) {
        let filtrosSalvos = JSON.parse(localStorage.getItem('filtrosRelatorioSalvos') || '[]');
        filtrosSalvos = filtrosSalvos.filter(f => f.nome !== nome);
        
        localStorage.setItem('filtrosRelatorioSalvos', JSON.stringify(filtrosSalvos));
        atualizarListaFiltrosSalvos();
        
        alert('Filtro removido: ' + nome);
    }
}

// Controlar exibição dos campos de data personalizada
function controlarCamposDataPersonalizada() {
    const periodo = document.getElementById('filtro-periodo-relatorio').value;
    const dataInicioContainer = document.getElementById('data-inicio-container');
    const dataFimContainer = document.getElementById('data-fim-container');
    
    if (periodo === 'personalizado') {
        dataInicioContainer.style.display = 'block';
        dataFimContainer.style.display = 'block';
    } else {
        dataInicioContainer.style.display = 'none';
        dataFimContainer.style.display = 'none';
    }
}

// Mostrar indicador de carregamento
function mostrarCarregandoRelatorio(mostrar) {
    const tabela = document.getElementById('tabela-preview-relatorio');
    
    if (mostrar) {
        tabela.innerHTML = '<tr><td colspan="8" class="text-center">' +
                          '<i class="fas fa-spinner fa-spin fa-2x text-primary mb-2 d-block"></i>' +
                          'Carregando dados...</td></tr>';
    }
}

// Gerar dados simulados baseados nos filtros
function gerarDadosSimuladosRelatorio(filtros) {
    // Simular dados baseados nos filtros
    const baseRegistros = Math.floor(Math.random() * 100) + 20;
    const registros = [];
    const usuarios = ['Admin', 'Auditor1', 'Operador1', 'Operador2'];
    const tipos = ['Automático', 'Manual', 'Correção'];
    const status = ['Concluído', 'Em Andamento', 'Com Erro'];
    
    for (let i = 0; i < Math.min(baseRegistros, 10); i++) {
        registros.push({
            id: 'REL' + (1000 + i),
            data: new Date(Date.now() - Math.random() * 30 * 24 * 60 * 60 * 1000).toLocaleDateString('pt-BR'),
            usuario: usuarios[Math.floor(Math.random() * usuarios.length)],
            tipo: tipos[Math.floor(Math.random() * tipos.length)],
            status: status[Math.floor(Math.random() * status.length)],
            valor: (Math.random() * 10000).toFixed(2),
            divergencias: Math.floor(Math.random() * 5),
            arquivo: 'arquivo_' + (i + 1) + '.csv'
        });
    }
    
    const estatisticas = {
        total: baseRegistros,
        conciliados: Math.floor(baseRegistros * 0.8),
        divergencias: Math.floor(baseRegistros * 0.15),
        valorTotal: (Math.random() * 100000).toFixed(2)
    };
    
    return { registros, estatisticas };
}

// Atualizar estatísticas do relatório
function atualizarEstatisticasRelatorio(stats) {
    // Tentar encontrar os elementos com os IDs corretos
    const totalElement = document.getElementById('total-registros-relatorio') || document.getElementById('total-registros');
    const conciliadosElement = document.getElementById('total-conciliados-relatorio') || document.getElementById('total-conciliados');
    const divergenciasElement = document.getElementById('total-divergencias-relatorio') || document.getElementById('total-divergencias');
    const valorElement = document.getElementById('valor-total-relatorio') || document.getElementById('valor-total');
    
    if (totalElement) totalElement.textContent = stats.total + ' registros';
    if (conciliadosElement) conciliadosElement.textContent = stats.conciliados + ' conciliados';
    if (divergenciasElement) divergenciasElement.textContent = stats.divergencias + ' divergências';
    if (valorElement) valorElement.textContent = 'R$ ' + parseFloat(stats.valorTotal).toLocaleString('pt-BR', { minimumFractionDigits: 2 });
}

// Atualizar tabela de preview
function atualizarTabelaPreviewRelatorio(registros) {
    const tabela = document.getElementById('tabela-preview-relatorio');
    
    if (registros.length === 0) {
        tabela.innerHTML = '<tr><td colspan="8" class="text-center text-muted">' +
                          '<i class="fas fa-search fa-2x mb-2 d-block"></i>' +
                          'Nenhum registro encontrado com os filtros aplicados</td></tr>';
        return;
    }
    
    tabela.innerHTML = registros.map(reg => 
        '<tr>' +
        '<td><strong>' + reg.id + '</strong></td>' +
        '<td>' + reg.data + '</td>' +
        '<td>' + reg.usuario + '</td>' +
        '<td><span class="badge bg-info">' + reg.tipo + '</span></td>' +
        '<td><span class="badge bg-' + (reg.status === 'Concluído' ? 'success' : reg.status === 'Em Andamento' ? 'warning' : 'danger') + '">' + reg.status + '</span></td>' +
        '<td>R$ ' + parseFloat(reg.valor).toLocaleString('pt-BR', { minimumFractionDigits: 2 }) + '</td>' +
        '<td>' + (reg.divergencias > 0 ? '<span class="badge bg-warning">' + reg.divergencias + '</span>' : '<span class="text-success">✓</span>') + '</td>' +
        '<td><small>' + reg.arquivo + '</small></td>' +
        '</tr>'
    ).join('');
}

// Limpar resultados
function limparResultadosRelatorio() {
    document.getElementById('total-registros-relatorio').textContent = '0';
    document.getElementById('total-conciliados-relatorio').textContent = '0';
    document.getElementById('total-divergencias-relatorio').textContent = '0';
    document.getElementById('valor-total-relatorio').textContent = 'R$ 0,00';
    
    document.getElementById('tabela-preview-relatorio').innerHTML = 
        '<tr><td colspan="8" class="text-center text-muted">' +
        '<i class="fas fa-search fa-2x mb-2 d-block"></i>' +
        'Aplique os filtros para visualizar os dados</td></tr>';
}

// Funções de exportação aprimoradas
function gerarRelatorioPDFCompleto() {
    const filtros = coletarFiltrosRelatorio();
    console.log('📄 Gerando relatório PDF com filtros:', filtros);
    alert('Gerando relatório PDF completo...\n\nEm breve será integrado com o backend para geração real do PDF.');
}

function exportarExcelCompleto() {
    const filtros = coletarFiltrosRelatorio();
    console.log('📊 Exportando Excel com filtros:', filtros);
    alert('Exportando dados para Excel...\n\nEm breve será integrado com o backend para exportação real.');
}

function abrirDashboardAnalitico() {
    console.log('📈 Abrindo dashboard analítico...');
    alert('Abrindo dashboard analítico...\n\nEm breve será implementado com gráficos interativos usando Chart.js ou similar.');
}

// Funções de exportação rápida
function exportarCSVRapido() {
    console.log('📄 Exportando CSV rápido...');
    
    const filtros = coletarFiltrosRelatorio();
    const dados = gerarDadosSimuladosRelatorio(filtros);
    
    // Criar CSV
    let csv = 'ID,Data,Usuario,Tipo,Status,Valor,Divergencias,Arquivo\n';
    dados.registros.forEach(reg => {
        csv += reg.id + ',' + reg.data + ',' + reg.usuario + ',' + reg.tipo + ',' + 
               reg.status + ',' + reg.valor + ',' + reg.divergencias + ',' + reg.arquivo + '\n';
    });
    
    // Download do arquivo
    const blob = new Blob([csv], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'relatorio_' + new Date().toISOString().slice(0, 10) + '.csv';
    a.click();
    window.URL.revokeObjectURL(url);
    
    alert('Arquivo CSV baixado com sucesso!');
}

function exportarJSONRapido() {
    console.log('📄 Exportando JSON...');
    
    const filtros = coletarFiltrosRelatorio();
    const dados = gerarDadosSimuladosRelatorio(filtros);
    
    const jsonData = {
        filtros: filtros,
        estatisticas: dados.estatisticas,
        registros: dados.registros,
        exportadoEm: new Date().toISOString(),
        versao: '1.0'
    };
    
    // Download do arquivo
    const blob = new Blob([JSON.stringify(jsonData, null, 2)], { type: 'application/json' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'relatorio_' + new Date().toISOString().slice(0, 10) + '.json';
    a.click();
    window.URL.revokeObjectURL(url);
    
    alert('Arquivo JSON baixado com sucesso!');
}

// Melhorar indicador de carregamento
function mostrarCarregandoRelatorio(mostrar) {
    const tabela = document.getElementById('tabela-preview-relatorio');
    const btnAplicar = document.getElementById('btn-aplicar-filtros');
    
    if (mostrar) {
        tabela.innerHTML = '<tr><td colspan="8" class="text-center">' +
                          '<div class="d-flex flex-column align-items-center py-4">' +
                          '<div class="spinner-border text-primary mb-3" role="status"></div>' +
                          '<h6 class="text-primary">Processando filtros...</h6>' +
                          '<small class="text-muted">Analisando dados do sistema</small>' +
                          '</div></td></tr>';
        
        if (btnAplicar) {
            btnAplicar.innerHTML = '<i class="fas fa-spinner fa-spin me-1"></i>Processando...';
            btnAplicar.disabled = true;
        }
    } else {
        if (btnAplicar) {
            btnAplicar.innerHTML = '<i class="fas fa-search me-1"></i>Filtrar';
            btnAplicar.disabled = false;
        }
    }
}

// Event listener para controlar campos de data personalizada
document.addEventListener('DOMContentLoaded', function() {
    const periodoSelect = document.getElementById('filtro-periodo-relatorio');
    if (periodoSelect) {
        periodoSelect.addEventListener('change', controlarCamposDataPersonalizada);
    }
    
    // Carregar filtros salvos na inicialização
    setTimeout(() => {
        atualizarListaFiltrosSalvos();
    }, 500);
});

// Sistema de filtros salvos aprimorado
function salvarFiltroPersonalizado() {
    const nome = prompt('Nome para o filtro personalizado:');
    if (!nome) return;
    
    const filtros = coletarFiltrosRelatorio();
    const filtrosSalvos = JSON.parse(localStorage.getItem('filtros_salvos') || '{}');
    
    filtrosSalvos[nome] = {
        ...filtros,
        salvoEm: new Date().toISOString(),
        usadoEm: new Date().toISOString(),
        contadorUso: 0
    };
    
    localStorage.setItem('filtros_salvos', JSON.stringify(filtrosSalvos));
    atualizarListaFiltrosSalvos();
    
    alert(`Filtro "${nome}" salvo com sucesso!`);
}

function carregarFiltroSalvo(nome) {
    const filtrosSalvos = JSON.parse(localStorage.getItem('filtros_salvos') || '{}');
    if (!filtrosSalvos[nome]) return;
    
    const filtro = filtrosSalvos[nome];
    
    // Aplicar filtros aos campos
    const campos = {
        'periodo-relatorio': filtro.periodo,
        'data-inicio': filtro.dataInicio,
        'data-fim': filtro.dataFim,
        'usuario-filtro': filtro.usuario,
        'tipo-filtro': filtro.tipo,
        'status-filtro': filtro.status,
        'valor-min': filtro.valorMin,
        'valor-max': filtro.valorMax,
        'divergencias-filtro': filtro.divergencias,
        'arquivo-filtro': filtro.arquivo
    };
    
    Object.keys(campos).forEach(id => {
        const elemento = document.getElementById(id);
        if (elemento && campos[id] !== undefined) {
            elemento.value = campos[id];
        }
    });
    
    // Atualizar contador de uso
    filtro.usadoEm = new Date().toISOString();
    filtro.contadorUso = (filtro.contadorUso || 0) + 1;
    filtrosSalvos[nome] = filtro;
    localStorage.setItem('filtros_salvos', JSON.stringify(filtrosSalvos));
    
    // Aplicar automaticamente
    aplicarFiltrosRelatorio();
    atualizarListaFiltrosSalvos();
    
    console.log(`✅ Filtro "${nome}" carregado e aplicado`);
}

function excluirFiltroSalvo(nome) {
    if (!confirm(`Tem certeza que deseja excluir o filtro "${nome}"?`)) return;
    
    const filtrosSalvos = JSON.parse(localStorage.getItem('filtros_salvos') || '{}');
    delete filtrosSalvos[nome];
    localStorage.setItem('filtros_salvos', JSON.stringify(filtrosSalvos));
    
    atualizarListaFiltrosSalvos();
    alert(`Filtro "${nome}" excluído com sucesso!`);
}

function atualizarListaFiltrosSalvos() {
    const filtrosSalvos = JSON.parse(localStorage.getItem('filtros_salvos') || '{}');
    const lista = document.getElementById('lista-filtros-salvos');
    
    if (!lista) return;
    
    if (Object.keys(filtrosSalvos).length === 0) {
        lista.innerHTML = '<small class="text-muted">Nenhum filtro salvo</small>';
        return;
    }
    
    let html = '';
    Object.keys(filtrosSalvos).sort().forEach(nome => {
        const filtro = filtrosSalvos[nome];
        const usado = filtro.contadorUso || 0;
        const dataSalvo = new Date(filtro.salvoEm).toLocaleDateString('pt-BR');
        
        html += `
            <div class="d-flex justify-content-between align-items-center mb-2 p-2 bg-light rounded">
                <div>
                    <strong>${nome}</strong>
                    <br><small class="text-muted">Salvo em: ${dataSalvo} | Usado: ${usado}x</small>
                </div>
                <div class="btn-group btn-group-sm">
                    <button class="btn btn-primary" onclick="carregarFiltroSalvo('${nome}')" title="Aplicar filtro">
                        <i class="fas fa-play"></i>
                    </button>
                    <button class="btn btn-danger" onclick="excluirFiltroSalvo('${nome}')" title="Excluir filtro">
                        <i class="fas fa-trash"></i>
                    </button>
                </div>
            </div>
        `;
    });
    
    lista.innerHTML = html;
}

// Função para limpar todos os filtros
function limparTodosFiltros() {
    const campos = [
        'periodo-relatorio', 'data-inicio', 'data-fim', 'usuario-filtro',
        'tipo-filtro', 'status-filtro', 'valor-min', 'valor-max',
        'divergencias-filtro', 'arquivo-filtro'
    ];
    
    campos.forEach(id => {
        const elemento = document.getElementById(id);
        if (elemento) {
            elemento.value = '';
        }
    });
    
    // Limpar tabela de preview
    const tabela = document.getElementById('tabela-preview-relatorio');
    if (tabela) {
        tabela.innerHTML = '<tr><td colspan="8" class="text-center text-muted">Configure os filtros acima e clique em "Filtrar" para visualizar os dados</td></tr>';
    }
    
    // Limpar estatísticas
    atualizarEstatisticasRelatorio({
        total: 0,
        conciliados: 0,
        divergencias: 0,
        valorTotal: '0.00'
    });
    
    console.log('🧹 Todos os filtros foram limpos');
}

// Gerar relatório de conciliação
function gerarRelatorioConciliacao() {
    console.log('📊 Gerando relatório de conciliação...');
    
    // Simular geração de relatório
    const loading = document.createElement('div');
    loading.innerHTML = `
        <div class="position-fixed top-0 start-0 w-100 h-100 d-flex align-items-center justify-content-center" 
             style="background: rgba(0,0,0,0.8); z-index: 9999;">
            <div class="card p-4 text-center">
                <div class="spinner-border text-primary mb-3" role="status"></div>
                <h5>Gerando Relatório de Conciliação</h5>
                <p class="text-muted">Processando dados e aplicando filtros...</p>
            </div>
        </div>
    `;
    document.body.appendChild(loading);
    
    setTimeout(() => {
        document.body.removeChild(loading);
        
        // Simular dados do relatório
        const relatorio = {
            periodo: 'Últimos 30 dias',
            totalRegistros: Math.floor(Math.random() * 1000) + 500,
            conciliados: Math.floor(Math.random() * 800) + 400,
            pendentes: Math.floor(Math.random() * 100) + 50,
            divergencias: Math.floor(Math.random() * 50) + 10,
            valorTotal: (Math.random() * 1000000).toFixed(2),
            geradoEm: new Date().toLocaleString('pt-BR')
        };
        
        const mensagem = `
            📊 RELATÓRIO DE CONCILIAÇÃO GERADO
            
            Período: ${relatorio.periodo}
            Data/Hora: ${relatorio.geradoEm}
            
            📈 ESTATÍSTICAS:
            • Total de Registros: ${relatorio.totalRegistros}
            • Conciliados: ${relatorio.conciliados} (${((relatorio.conciliados/relatorio.totalRegistros)*100).toFixed(1)}%)
            • Pendentes: ${relatorio.pendentes}
            • Divergências: ${relatorio.divergencias} (${((relatorio.divergencias/relatorio.totalRegistros)*100).toFixed(1)}%)
            • Valor Total: R$ ${parseFloat(relatorio.valorTotal).toLocaleString('pt-BR')}
            
            O relatório foi gerado com sucesso! 
            Em um sistema real, este seria salvo como arquivo PDF ou Excel.
        `;
        
        alert(mensagem);
    }, 2000);
}
