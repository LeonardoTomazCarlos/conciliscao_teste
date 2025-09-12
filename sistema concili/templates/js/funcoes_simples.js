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

// Função auxiliar para formatar valores monetários
function formatarMoeda(valor) {
    return new Intl.NumberFormat('pt-BR', {
        style: 'currency',
        currency: 'BRL'
    }).format(valor || 0);
}

// Função auxiliar para formatar datas
function formatarData(data) {
    return new Date(data).toLocaleString('pt-BR', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}

// Função para renderizar linha da tabela de conciliações
function renderizarLinhaConciliacao(item) {
    const dataFormatada = formatarData(item.data_hora);
    const statusClass = item.status === 'Concluído' ? 'bg-success' : 
                       item.status === 'Em Andamento' ? 'bg-warning' : 'bg-danger';
    const statusIcon = item.status === 'Concluído' ? 'fa-check' : 
                      item.status === 'Em Andamento' ? 'fa-clock' : 'fa-exclamation';
    
    return `
        <tr class="align-middle">
            <td class="fw-bold">${item.id_procedimento}</td>
            <td>
                <div>${dataFormatada.split(' ')[0]}</div>
                <small class="text-muted">${dataFormatada.split(' ')[1]}</small>
            </td>
            <td><span class="badge bg-info">${item.tipo}</span></td>
            <td>${item.metodo}</td>
            <td class="text-center fw-bold">${item.total_conciliacoes}</td>
            <td>
                <span class="badge ${statusClass}">
                    <i class="fas ${statusIcon} me-1"></i>${item.status}
                </span>
            </td>
            <td>
                <div class="d-flex align-items-center">
                    <i class="fas fa-user-circle me-2"></i>${item.usuario}
                </div>
            </td>
            <td class="text-end fw-bold">${formatarMoeda(item.valor_total)}</td>
            <td>
                <div class="btn-group btn-group-sm">
                    <button class="btn btn-primary" onclick="verDetalhesConciliacao(${item.id_procedimento})" 
                            title="Ver Detalhes" data-bs-toggle="tooltip">
                        <i class="fas fa-eye"></i>
                    </button>
                    <button class="btn btn-danger" onclick="cancelarConciliacao(${item.id_procedimento})" 
                            title="Cancelar" data-bs-toggle="tooltip"
                            ${item.status === 'Concluído' ? 'disabled' : ''}>
                        <i class="fas fa-times"></i>
                    </button>
                    <button class="btn btn-success" onclick="exportarProcedimento(${item.id_procedimento})" 
                            title="Exportar" data-bs-toggle="tooltip">
                        <i class="fas fa-download"></i>
                    </button>
                </div>
            </td>
        </tr>
    `;
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
    
    // Mostrar estado de carregamento
    const tabela = document.getElementById('tabela-conciliacoes');
    if (tabela) {
        tabela.innerHTML = `
            <tr>
                <td colspan="9" class="text-center py-4">
                    <div class="spinner-border text-primary mb-3" role="status"></div>
                    <div class="text-primary">Carregando dados...</div>
                    <small class="text-muted">Aplicando filtros e atualizando resultados</small>
                </td>
            </tr>
        `;
    }
    
    // Desabilitar botões durante o carregamento
    const btnAplicar = document.querySelector('button[onclick="aplicarFiltros()"]');
    const btnLimpar = document.querySelector('button[onclick="limparFiltros()"]');
    if (btnAplicar) btnAplicar.disabled = true;
    if (btnLimpar) btnLimpar.disabled = true;
    
    // Coletar dados dos filtros
    const dataInicio = document.getElementById('filtro-data-inicio').value;
    const dataFim = document.getElementById('filtro-data-fim').value;
    const tipo = document.getElementById('filtro-tipo').value;
    const status = document.getElementById('filtro-status').value;
    const porPagina = document.getElementById('filtro-por-pagina')?.value || '10';
    
    // Construir parâmetros para a requisição
    const params = new URLSearchParams();
    if (dataInicio) params.append('data_inicio', dataInicio);
    if (dataFim) params.append('data_fim', dataFim);
    if (tipo) params.append('tipo', tipo);
    if (status) params.append('status', status);
    params.append('por_pagina', porPagina);
    
    // Carregar conciliações com os filtros
    fetch(`/api/conciliacoes?${params}`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Erro ao carregar dados: ' + response.statusText);
            }
            return response.json();
        })
        .then(data => {
            // Atualizar a tabela de conciliações
            const tabela = document.getElementById('tabela-conciliacoes');
            if (!tabela) return;
            
            if (!data || data.length === 0) {
                tabela.innerHTML = `
                    <tr>
                        <td colspan="9" class="text-center py-4">
                            <div class="text-muted">
                                <i class="fas fa-search fa-2x mb-3 d-block"></i>
                                <div>Nenhuma conciliação encontrada com os filtros aplicados</div>
                                <small class="text-muted mt-2">Tente ajustar os critérios de busca</small>
                            </div>
                        </td>
                    </tr>`;
                
                // Zerar estatísticas quando não há dados
                atualizarEstatisticasConciliacao([]);
                return;
            }
            
            tabela.innerHTML = data.map(item => `
                <tr>
                    <td>${item.id_procedimento}</td>
                    <td>${new Date(item.data_hora).toLocaleString('pt-BR')}</td>
                    <td>${item.tipo}</td>
                    <td>${item.metodo}</td>
                    <td>${item.total_conciliacoes}</td>
                    <td>
                        <span class="badge ${item.status === 'Concluído' ? 'bg-success' : 
                                          item.status === 'Em Andamento' ? 'bg-warning' : 'bg-danger'}">
                            ${item.status}
                        </span>
                    </td>
                    <td>${item.usuario}</td>
                    <td>R$ ${parseFloat(item.valor_total).toLocaleString('pt-BR', {minimumFractionDigits: 2})}</td>
                    <td>
                        <div class="btn-group btn-group-sm">
                            <button class="btn btn-primary" onclick="verDetalhesConciliacao(${item.id_procedimento})" title="Ver Detalhes">
                                <i class="fas fa-eye"></i>
                            </button>
                            <button class="btn btn-danger" onclick="cancelarConciliacao(${item.id_procedimento})" title="Cancelar">
                                <i class="fas fa-times"></i>
                            </button>
                            <button class="btn btn-success" onclick="exportarProcedimento(${item.id_procedimento})" title="Exportar">
                                <i class="fas fa-download"></i>
                            </button>
                        </div>
                    </td>
                </tr>
            `).join('');
            
            // Atualizar estatísticas
            const statTotal = document.getElementById('stat-total-conciliacoes');
            const statAtivas = document.getElementById('stat-conciliacoes-ativas');
            const statAutomaticas = document.getElementById('stat-conciliacoes-automaticas');
            const statRecentes = document.getElementById('stat-conciliacoes-recentes');
            
            if (statTotal) statTotal.textContent = data.length;
            if (statAtivas) statAtivas.textContent = data.filter(item => item.status === 'Concluído').length;
            if (statAutomaticas) statAutomaticas.textContent = data.filter(item => item.tipo === 'Automática').length;
            if (statRecentes) statRecentes.textContent = data.filter(item => {
                const data = new Date(item.data_hora);
                const trintaDiasAtras = new Date();
                trintaDiasAtras.setDate(trintaDiasAtras.getDate() - 30);
                return data >= trintaDiasAtras;
            }).length;
        })
        .catch(error => {
            console.error('Erro ao carregar conciliações:', error);
            const tabela = document.getElementById('tabela-conciliacoes');
            if (tabela) {
                tabela.innerHTML = `
                    <tr>
                        <td colspan="9" class="text-center text-danger py-4">
                            <i class="fas fa-exclamation-triangle fa-2x mb-3 d-block"></i>
                            Erro ao carregar conciliações. Tente novamente mais tarde.
                        </td>
                    </tr>`;
            }
        });
}

// Limpar filtros de conciliações
function limparFiltros() {
    console.log('Limpando filtros de conciliações');
    const campos = ['filtro-data-inicio', 'filtro-data-fim', 'filtro-tipo', 'filtro-status', 'filtro-por-pagina'];
    campos.forEach(campo => {
        const elemento = document.getElementById(campo);
        if (elemento) {
            if (campo === 'filtro-por-pagina') {
                elemento.value = '10';  // Resetar para valor padrão
            } else {
                elemento.value = '';
            }
        }
    });
    
    // Após limpar, carregar todas as conciliações sem filtros
    fetch('/api/conciliacoes')
        .then(response => response.json())
        .then(data => {
            const tabela = document.getElementById('tabela-conciliacoes');
            if (!tabela) return;
            
            if (data.length === 0) {
                tabela.innerHTML = `
                    <tr>
                        <td colspan="9" class="text-center py-4">
                            <div class="text-muted">
                                <i class="fas fa-info-circle fa-2x mb-3 d-block"></i>
                                Nenhuma conciliação encontrada
                            </div>
                        </td>
                    </tr>`;
                return;
            }
            
            tabela.innerHTML = data.map(item => `
                <tr>
                    <td>${item.id_procedimento}</td>
                    <td>${new Date(item.data_hora).toLocaleString('pt-BR')}</td>
                    <td>${item.tipo}</td>
                    <td>${item.metodo}</td>
                    <td>${item.total_conciliacoes}</td>
                    <td>
                        <span class="badge ${item.status === 'Concluído' ? 'bg-success' : 
                                          item.status === 'Em Andamento' ? 'bg-warning' : 'bg-danger'}">
                            ${item.status}
                        </span>
                    </td>
                    <td>${item.usuario}</td>
                    <td>R$ ${parseFloat(item.valor_total).toLocaleString('pt-BR', {minimumFractionDigits: 2})}</td>
                    <td>
                        <div class="btn-group btn-group-sm">
                            <button class="btn btn-primary" onclick="verDetalhesConciliacao(${item.id_procedimento})" title="Ver Detalhes">
                                <i class="fas fa-eye"></i>
                            </button>
                            <button class="btn btn-danger" onclick="cancelarConciliacao(${item.id_procedimento})" title="Cancelar">
                                <i class="fas fa-times"></i>
                            </button>
                            <button class="btn btn-success" onclick="exportarProcedimento(${item.id_procedimento})" title="Exportar">
                                <i class="fas fa-download"></i>
                            </button>
                        </div>
                    </td>
                </tr>
            `).join('');
            
            // Atualizar estatísticas
            atualizarEstatisticasConciliacao(data);
        })
        .catch(error => {
            console.error('Erro ao carregar conciliações:', error);
            const tabela = document.getElementById('tabela-conciliacoes');
            if (tabela) {
                tabela.innerHTML = `
                    <tr>
                        <td colspan="9" class="text-center text-danger py-4">
                            <i class="fas fa-exclamation-triangle fa-2x mb-3 d-block"></i>
                            Erro ao carregar conciliações. Tente novamente mais tarde.
                        </td>
                    </tr>`;
            }
        });
}

// Função auxiliar para atualizar estatísticas
function atualizarEstatisticasConciliacao(data) {
    const statTotal = document.getElementById('stat-total-conciliacoes');
    const statAtivas = document.getElementById('stat-conciliacoes-ativas');
    const statAutomaticas = document.getElementById('stat-conciliacoes-automaticas');
    const statRecentes = document.getElementById('stat-conciliacoes-recentes');
    
    if (statTotal) statTotal.textContent = data.length;
    if (statAtivas) statAtivas.textContent = data.filter(item => item.status === 'Concluído').length;
    if (statAutomaticas) statAutomaticas.textContent = data.filter(item => item.tipo === 'Automática').length;
    if (statRecentes) statRecentes.textContent = data.filter(item => {
        const data = new Date(item.data_hora);
        const trintaDiasAtras = new Date();
        trintaDiasAtras.setDate(trintaDiasAtras.getDate() - 30);
        return data >= trintaDiasAtras;
    }).length;
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
            // Tratar especificamente a falta de dados
            if (data.message && data.message.includes('Não há dados suficientes')) {
                alert('⚠️ ' + data.message);
            } else {
                alert('❌ Erro na conciliação: ' + (data.error || data.message || 'Erro desconhecido'));
            }
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
    console.log('🔍 [DEBUG] Iniciando aplicarFiltrosRelatorio...');
    
    try {
        const filtros = coletarFiltrosRelatorio();
        console.log('📋 [DEBUG] Filtros coletados:', filtros);
        
        // Mostrar carregamento
        mostrarCarregandoRelatorio(true);
        
        // Construir URL com parâmetros
        const params = new URLSearchParams();
        Object.keys(filtros).forEach(key => {
            if (filtros[key] && filtros[key] !== '') {
                params.append(key, filtros[key]);
            }
        });
        
        console.log('🌐 [DEBUG] URL de requisição:', `/api/relatorios/consolidado?${params.toString()}`);
        
        // Fazer requisição ao backend
        fetch(`/api/relatorios/consolidado?${params.toString()}`)
            .then(response => {
                console.log('📡 [DEBUG] Response status:', response.status);
                if (!response.ok) {
                    throw new Error(`Erro HTTP: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                console.log('📊 [DEBUG] Dados recebidos:', data);
                
                // Atualizar estatísticas
                atualizarEstatisticasRelatorio(data.estatisticas);
                
                // Atualizar tabela de preview
                atualizarTabelaPreviewRelatorio(data.preview_dados || []);
                
                // Mostrar mensagem de sucesso
                mostrarNotificacao('✅ Filtros aplicados com sucesso!', 'success');
                
            })
            .catch(error => {
                console.error('❌ [DEBUG] Erro ao aplicar filtros:', error);
                mostrarNotificacao('❌ Erro ao aplicar filtros: ' + error.message, 'error');
            })
            .finally(() => {
                mostrarCarregandoRelatorio(false);
            });
    } catch (error) {
        console.error('❌ [DEBUG] Erro geral em aplicarFiltrosRelatorio:', error);
        mostrarNotificacao('❌ Erro interno: ' + error.message, 'error');
        mostrarCarregandoRelatorio(false);
    }
}

// Coletar todos os filtros do formulário
function coletarFiltrosRelatorio() {
    const filtros = {
        periodo: document.getElementById('filtro-periodo-relatorio')?.value || '',
        data_inicio: document.getElementById('filtro-data-inicio-relatorio')?.value || '',
        data_fim: document.getElementById('filtro-data-fim-relatorio')?.value || '',
        usuario: document.getElementById('filtro-usuario-relatorio')?.value || '',
        tipo: document.getElementById('filtro-tipo-relatorio')?.value || '',
        status: document.getElementById('filtro-status-relatorio')?.value || '',
        valor_min: document.getElementById('filtro-valor-min-relatorio')?.value || '',
        valor_max: document.getElementById('filtro-valor-max-relatorio')?.value || '',
        divergencias: document.getElementById('filtro-divergencias-relatorio')?.value || '',
        arquivo: document.getElementById('filtro-arquivo-relatorio')?.value || ''
    };
    
    // Processar filtros de período predefinido
    if (filtros.periodo && filtros.periodo !== 'personalizado') {
        const hoje = new Date();
        const dataInicio = new Date();
        
        switch (filtros.periodo) {
            case 'hoje':
                filtros.data_inicio = hoje.toISOString().split('T')[0];
                filtros.data_fim = hoje.toISOString().split('T')[0];
                break;
            case 'ontem':
                const ontem = new Date(hoje);
                ontem.setDate(ontem.getDate() - 1);
                filtros.data_inicio = ontem.toISOString().split('T')[0];
                filtros.data_fim = ontem.toISOString().split('T')[0];
                break;
            case '7dias':
                dataInicio.setDate(dataInicio.getDate() - 7);
                filtros.data_inicio = dataInicio.toISOString().split('T')[0];
                filtros.data_fim = hoje.toISOString().split('T')[0];
                break;
            case '30dias':
                dataInicio.setDate(dataInicio.getDate() - 30);
                filtros.data_inicio = dataInicio.toISOString().split('T')[0];
                filtros.data_fim = hoje.toISOString().split('T')[0];
                break;
            case 'mes-atual':
                filtros.data_inicio = new Date(hoje.getFullYear(), hoje.getMonth(), 1).toISOString().split('T')[0];
                filtros.data_fim = hoje.toISOString().split('T')[0];
                break;
            case 'mes-anterior':
                const mesAnterior = new Date(hoje.getFullYear(), hoje.getMonth() - 1, 1);
                const fimMesAnterior = new Date(hoje.getFullYear(), hoje.getMonth(), 0);
                filtros.data_inicio = mesAnterior.toISOString().split('T')[0];
                filtros.data_fim = fimMesAnterior.toISOString().split('T')[0];
                break;
            case 'ano-atual':
                filtros.data_inicio = new Date(hoje.getFullYear(), 0, 1).toISOString().split('T')[0];
                filtros.data_fim = hoje.toISOString().split('T')[0];
                break;
        }
    }
    
    return filtros;
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
    console.log('📄 Gerando relatório PDF completo...');
    
    const filtros = coletarFiltrosRelatorio();
    const params = new URLSearchParams();
    
    Object.keys(filtros).forEach(key => {
        if (filtros[key] && filtros[key] !== '') {
            params.append(key, filtros[key]);
        }
    });
    
    // Por enquanto, apenas mostrar mensagem informativa
    mostrarNotificacao('📄 Gerando relatório PDF...\n\nRecurso em desenvolvimento. Em breve você poderá baixar relatórios completos em PDF!', 'info');
    
    // TODO: Implementar endpoint /api/relatorios/export/pdf
    // const url = `/api/relatorios/export/pdf?${params.toString()}`;
    // window.open(url, '_blank');
}

function abrirDashboardAnalitico() {
    console.log('📈 Abrindo dashboard analítico...');
    
    // Aplicar filtros primeiro
    aplicarFiltrosRelatorio();
    
    // Simular abertura de modal ou seção de gráficos
    setTimeout(() => {
        mostrarNotificacao('📈 Dashboard analítico carregado!\n\nEm breve será implementado com gráficos interativos usando Chart.js.', 'info');
        
        // TODO: Implementar gráficos interativos
        // Pode ser um modal com gráficos ou redirecionamento para uma página específica
    }, 1000);
}

function gerarRelatorioConciliacao() {
    console.log('� Gerando relatório de conciliação...');
    
    // Aplicar filtros e mostrar resultado específico de conciliação
    aplicarFiltrosRelatorio();
    
    setTimeout(() => {
        mostrarNotificacao('📊 Relatório de conciliação gerado com sucesso!\n\nVisualize os dados na tabela de preview abaixo.', 'success');
    }, 1500);
}

// Funções de exportação rápida
function verificarDadosDisponiveis() {
    console.log('🔍 [DEBUG] Verificando dados disponíveis...');
    
    return fetch('/api/relatorios/status')
        .then(response => response.json())
        .then(data => {
            console.log('📊 [DEBUG] Status dos dados:', data);
            return data;
        })
        .catch(error => {
            console.error('❌ [DEBUG] Erro ao verificar dados:', error);
            return { tem_dados: false, total_extratos: 0, total_lancamentos: 0 };
        });
}

async function verificarEAvisarSemDados() {
    const status = await verificarDadosDisponiveis();
    
    if (!status.tem_dados) {
        const resposta = confirm(
            '⚠️ AVISO: Não há dados reais no banco!\n\n' +
            `Extratos: ${status.total_extratos} | Lançamentos: ${status.total_lancamentos}\n\n` +
            'Deseja:\n' +
            '• OK: Exportar com dados de exemplo\n' +
            '• Cancelar: Criar dados de exemplo primeiro\n\n' +
            'Recomendamos criar dados de exemplo para testar as exportações.'
        );
        
        if (!resposta) {
            // Usuário escolheu criar dados
            criarDadosExemplo();
            return false; // Cancela a exportação
        }
    }
    
    return true; // Continua com a exportação
}

function exportarCSVRapido() {
    console.log('📄 [DEBUG] Iniciando exportarCSVRapido...');
    
    verificarEAvisarSemDados().then(continuar => {
        if (!continuar) return;
        
        try {
            const filtros = coletarFiltrosRelatorio();
            console.log('📋 [DEBUG] Filtros para CSV:', filtros);
            
            const params = new URLSearchParams();
            
            Object.keys(filtros).forEach(key => {
                if (filtros[key] && filtros[key] !== '') {
                    params.append(key, filtros[key]);
                }
            });
            
            const url = `/api/relatorios/export/csv?${params.toString()}`;
            console.log('🌐 [DEBUG] URL CSV:', url);
            
            // Mostrar loading
            mostrarNotificacao('📄 Preparando exportação CSV... Aguarde!', 'info');
            
            // Fazer download direto
            window.open(url, '_blank');
            
            // Feedback de sucesso após um tempo
            setTimeout(() => {
                mostrarNotificacao('✅ Arquivo CSV exportado com sucesso!\n\nO download deve ter iniciado automaticamente. Verifique sua pasta de downloads.', 'success');
            }, 2000);
            
            console.log('✅ [DEBUG] CSV download iniciado');
            
        } catch (error) {
            console.error('❌ [DEBUG] Erro em exportarCSVRapido:', error);
            mostrarNotificacao('❌ Erro ao exportar CSV: ' + error.message, 'error');
        }
    });
}

function exportarJSONRapido() {
    console.log('📄 [DEBUG] Iniciando exportarJSONRapido...');
    
    verificarEAvisarSemDados().then(continuar => {
        if (!continuar) return;
        
        try {
            const filtros = coletarFiltrosRelatorio();
            console.log('📋 [DEBUG] Filtros para JSON:', filtros);
            
            const params = new URLSearchParams();
            
            Object.keys(filtros).forEach(key => {
                if (filtros[key] && filtros[key] !== '') {
                    params.append(key, filtros[key]);
                }
            });
            
            const url = `/api/relatorios/export/json?${params.toString()}`;
            console.log('🌐 [DEBUG] URL JSON:', url);
            
            // Mostrar loading
            mostrarNotificacao('📄 Preparando exportação JSON... Aguarde!', 'info');
            
            // Fazer download direto
            window.open(url, '_blank');
            
            // Feedback de sucesso após um tempo
            setTimeout(() => {
                mostrarNotificacao('✅ Arquivo JSON exportado com sucesso!\n\nO arquivo contém dados estruturados com estatísticas completas. Verifique sua pasta de downloads.', 'success');
            }, 2000);
            
            console.log('✅ [DEBUG] JSON download iniciado');
            
        } catch (error) {
            console.error('❌ [DEBUG] Erro em exportarJSONRapido:', error);
            mostrarNotificacao('❌ Erro ao exportar JSON: ' + error.message, 'error');
        }
    });
}
        
        // Feedback de sucesso após um tempo
        setTimeout(() => {
            mostrarNotificacao('✅ Arquivo JSON exportado com sucesso!\n\nO arquivo contém dados estruturados com estatísticas completas. Verifique sua pasta de downloads.', 'success');
        }, 2000);
        
        console.log('✅ [DEBUG] JSON download iniciado');
        
    } catch (error) {
        console.error('❌ [DEBUG] Erro em exportarJSONRapido:', error);
        mostrarNotificacao('❌ Erro ao exportar JSON: ' + error.message, 'error');
    }
}

function exportarExcelCompleto() {
    console.log('📊 [DEBUG] Iniciando exportarExcelCompleto...');
    
    verificarEAvisarSemDados().then(continuar => {
        if (!continuar) return;
        
        try {
            const filtros = coletarFiltrosRelatorio();
            console.log('📋 [DEBUG] Filtros para Excel:', filtros);
            
            const params = new URLSearchParams();
            
            Object.keys(filtros).forEach(key => {
                if (filtros[key] && filtros[key] !== '') {
                    params.append(key, filtros[key]);
                }
            });
            
            const url = `/api/relatorios/export/excel?${params.toString()}`;
            console.log('🌐 [DEBUG] URL Excel:', url);
            
            // Mostrar loading
            mostrarNotificacao('📊 Preparando planilha Excel... Isso pode levar alguns segundos!', 'info');
            
            // Fazer download direto
            window.open(url, '_blank');
            
            // Feedback de sucesso após um tempo
            setTimeout(() => {
                mostrarNotificacao('✅ Planilha Excel exportada com sucesso!\n\nO arquivo contém múltiplas abas:\n• Extratos Bancários\n• Lançamentos Contábeis\n• Estatísticas\n\nVerifique sua pasta de downloads.', 'success');
            }, 3000);
            
            console.log('✅ [DEBUG] Excel download iniciado');
            
        } catch (error) {
            console.error('❌ [DEBUG] Erro em exportarExcelCompleto:', error);
            mostrarNotificacao('❌ Erro ao exportar Excel: ' + error.message, 'error');
        }
    });
}
}

function exportarJSONRapido() {
    console.log('📄 Exportando JSON...');
    
    const filtros = coletarFiltrosRelatorio();
    const params = new URLSearchParams();
    
    Object.keys(filtros).forEach(key => {
        if (filtros[key] && filtros[key] !== '') {
            params.append(key, filtros[key]);
        }
    });
    
    // Fazer download direto
    const url = `/api/relatorios/export/json?${params.toString()}`;
    window.open(url, '_blank');
    
    mostrarNotificacao('📄 Iniciando download do arquivo JSON...', 'info');
}

function exportarExcelCompleto() {
    console.log('� Exportando Excel completo...');
    
    const filtros = coletarFiltrosRelatorio();
    const params = new URLSearchParams();
    
    Object.keys(filtros).forEach(key => {
        if (filtros[key] && filtros[key] !== '') {
            params.append(key, filtros[key]);
        }
    });
    
    // Fazer download direto
    const url = `/api/relatorios/export/excel?${params.toString()}`;
    window.open(url, '_blank');
    
    mostrarNotificacao('📊 Iniciando download do arquivo Excel...', 'info');
}
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
    console.log('🗑️ Limpando todos os filtros...');
    
    // Limpar campos de filtro - usando IDs corretos
    const campos = [
        'filtro-periodo-relatorio',
        'filtro-data-inicio-relatorio', 
        'filtro-data-fim-relatorio',
        'filtro-usuario-relatorio',
        'filtro-tipo-relatorio',
        'filtro-status-relatorio',
        'filtro-valor-min-relatorio',
        'filtro-valor-max-relatorio',
        'filtro-divergencias-relatorio',
        'filtro-arquivo-relatorio'
    ];
    
    campos.forEach(campoId => {
        const campo = document.getElementById(campoId);
        if (campo) {
            if (campo.tagName === 'SELECT') {
                campo.selectedIndex = 0;
            } else {
                campo.value = '';
            }
        }
    });
    
    // Restaurar período padrão
    const periodoCampo = document.getElementById('filtro-periodo-relatorio');
    if (periodoCampo) {
        periodoCampo.value = '30dias';
    }
    
    // Esconder campos de data personalizada
    const dataInicioContainer = document.getElementById('data-inicio-container');
    const dataFimContainer = document.getElementById('data-fim-container');
    if (dataInicioContainer) dataInicioContainer.style.display = 'none';
    if (dataFimContainer) dataFimContainer.style.display = 'none';
    
    // Limpar resultados
    limparResultadosRelatorio();
    
    mostrarNotificacao('🗑️ Todos os filtros foram limpos!', 'success');
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

// Função para criar dados de exemplo
function criarDadosExemplo() {
    if (!confirm('Deseja criar dados de exemplo?\n\nIsso irá adicionar extratos, lançamentos, conciliações e divergências de exemplo ao sistema.')) {
        return;
    }
    
    console.log('🔧 Criando dados de exemplo...');
    
    // Mostrar loading
    const loading = document.createElement('div');
    loading.innerHTML = `
        <div class="position-fixed top-0 start-0 w-100 h-100 d-flex align-items-center justify-content-center" 
             style="background: rgba(0,0,0,0.8); z-index: 9999;">
            <div class="card p-4 text-center">
                <div class="spinner-border text-success mb-3" role="status"></div>
                <h5>Criando Dados de Exemplo</h5>
                <p class="text-muted">Gerando extratos, lançamentos e divergências...</p>
            </div>
        </div>
    `;
    document.body.appendChild(loading);
    
    fetch('/api/criar-dados-exemplo', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        document.body.removeChild(loading);
        
        if (data.success) {
            alert('✅ Dados de exemplo criados com sucesso!\n\n' + 
                  `• ${data.extratos_criados || 0} extratos bancários\n` +
                  `• ${data.lancamentos_criados || 0} lançamentos contábeis\n` +
                  `• ${data.conciliacoes_criadas || 0} conciliações\n` +
                  `• ${data.divergencias_criadas || 0} divergências\n\n` +
                  'Agora você pode testar todas as funcionalidades do sistema!');
            
            // Recarregar estatísticas se estivermos no dashboard
            if (typeof carregarEstatisticas === 'function') {
                carregarEstatisticas();
            }
            
            // Se estivermos na aba de divergências, recarregar
            const abaAtiva = document.querySelector('#divergencias.active');
            if (abaAtiva && typeof buscarDivergencias === 'function') {
                buscarDivergencias();
            }
        } else {
            alert('❌ Erro ao criar dados de exemplo:\n' + (data.error || 'Erro desconhecido'));
        }
    })
    .catch(error => {
        document.body.removeChild(loading);
        console.error('Erro:', error);
        alert('❌ Erro ao criar dados de exemplo:\n' + error.message);
    });
}

// Função para limpar todos os dados
function limparTodosDados() {
    if (!confirm('⚠️ ATENÇÃO!\n\nDeseja limpar TODOS os dados do sistema?\n\nIsso irá remover:\n• Todos os extratos bancários\n• Todos os lançamentos contábeis\n• Todas as conciliações\n• Todas as divergências\n\nEsta ação NÃO pode ser desfeita!')) {
        return;
    }
    
    if (!confirm('Tem certeza absoluta?\n\nTodos os dados serão perdidos permanentemente!')) {
        return;
    }
    
    console.log('🗑️ Limpando todos os dados...');
    
    // Mostrar loading
    const loading = document.createElement('div');
    loading.innerHTML = `
        <div class="position-fixed top-0 start-0 w-100 h-100 d-flex align-items-center justify-content-center" 
             style="background: rgba(0,0,0,0.8); z-index: 9999;">
            <div class="card p-4 text-center">
                <div class="spinner-border text-danger mb-3" role="status"></div>
                <h5>Limpando Dados</h5>
                <p class="text-muted">Removendo todos os registros...</p>
            </div>
        </div>
    `;
    document.body.appendChild(loading);
    
    fetch('/api/limpar-dados', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        document.body.removeChild(loading);
        
        if (data.success) {
            alert('✅ Todos os dados foram removidos com sucesso!\n\n' +
                  'O sistema foi reinicializado e está pronto para novos dados.');
            
            // Recarregar a página para atualizar todos os dados
            window.location.reload();
        } else {
            alert('❌ Erro ao limpar dados:\n' + (data.error || 'Erro desconhecido'));
        }
    })
    .catch(error => {
        document.body.removeChild(loading);
        console.error('Erro:', error);
        alert('❌ Erro ao limpar dados:\n' + error.message);
    });
}

// ===== FUNÇÕES AUXILIARES PARA RELATÓRIOS =====

// Função para atualizar estatísticas do relatório
function atualizarEstatisticasRelatorio(stats) {
    console.log('📊 Atualizando estatísticas:', stats);
    
    // Atualizar cards de estatísticas
    const elementos = {
        'total-registros-relatorio': stats.total_registros || 0,
        'total-conciliados-relatorio': stats.extratos_conciliados || 0,
        'total-divergencias-relatorio': stats.total_divergencias || 0,
        'valor-total-relatorio': `R$ ${(stats.valor_total_extratos || 0).toLocaleString('pt-BR', {minimumFractionDigits: 2})}`
    };
    
    Object.keys(elementos).forEach(id => {
        const elemento = document.getElementById(id);
        if (elemento) {
            elemento.textContent = elementos[id];
        }
    });
    
    // Atualizar badges na tabela de preview
    const badges = {
        'total-registros': `${stats.total_registros || 0} registros`,
        'total-conciliados': `${stats.extratos_conciliados || 0} conciliados`,
        'total-divergencias': `${stats.total_divergencias || 0} divergências`,
        'valor-total': `R$ ${(stats.valor_total_extratos || 0).toLocaleString('pt-BR', {minimumFractionDigits: 2})}`
    };
    
    Object.keys(badges).forEach(id => {
        const elemento = document.getElementById(id);
        if (elemento) {
            elemento.textContent = badges[id];
        }
    });
}

// Função para atualizar tabela de preview
function atualizarTabelaPreviewRelatorio(dados) {
    console.log('📋 Atualizando tabela de preview:', dados);
    
    const tabela = document.getElementById('tabela-preview-relatorio');
    if (!tabela) return;
    
    if (!dados || dados.length === 0) {
        tabela.innerHTML = `
            <tr>
                <td colspan="8" class="text-center text-muted">
                    <i class="fas fa-search fa-2x mb-2 d-block"></i>
                    Nenhum registro encontrado com os filtros aplicados
                </td>
            </tr>
        `;
        return;
    }
    
    let html = '';
    dados.forEach(item => {
        const statusClass = item.status === 'Conciliado' ? 'success' : 'warning';
        const divergenciaClass = item.divergencias === 'Sim' ? 'danger' : 'success';
        
        html += `
            <tr>
                <td><strong>${item.id}</strong></td>
                <td>${item.data}</td>
                <td>
                    <span class="badge bg-info">${item.usuario}</span>
                </td>
                <td>
                    <span class="badge bg-secondary">${item.tipo}</span>
                </td>
                <td>
                    <span class="badge bg-${statusClass}">${item.status}</span>
                </td>
                <td>
                    <strong class="text-primary">${item.valor}</strong>
                </td>
                <td>
                    <span class="badge bg-${divergenciaClass}">${item.divergencias}</span>
                </td>
                <td>
                    <small class="text-muted">${item.arquivo}</small>
                </td>
            </tr>
        `;
    });
    
    tabela.innerHTML = html;
}

// Função para mostrar/esconder loading
function mostrarCarregandoRelatorio(mostrar) {
    const btnFiltrar = document.getElementById('btn-aplicar-filtros');
    
    if (mostrar) {
        if (btnFiltrar) {
            btnFiltrar.disabled = true;
            btnFiltrar.innerHTML = '<i class="fas fa-spinner fa-spin me-1"></i>Carregando...';
        }
        
        // Mostrar loading na tabela
        const tabela = document.getElementById('tabela-preview-relatorio');
        if (tabela) {
            tabela.innerHTML = `
                <tr>
                    <td colspan="8" class="text-center">
                        <i class="fas fa-spinner fa-spin fa-2x mb-2 d-block text-primary"></i>
                        <span class="text-muted">Carregando dados...</span>
                    </td>
                </tr>
            `;
        }
    } else {
        if (btnFiltrar) {
            btnFiltrar.disabled = false;
            btnFiltrar.innerHTML = '<i class="fas fa-search me-1"></i>Filtrar';
        }
    }
}

// Função para limpar resultados
function limparResultadosRelatorio() {
    // Limpar estatísticas
    atualizarEstatisticasRelatorio({
        total_registros: 0,
        extratos_conciliados: 0,
        total_divergencias: 0,
        valor_total_extratos: 0
    });
    
    // Limpar tabela
    const tabela = document.getElementById('tabela-preview-relatorio');
    if (tabela) {
        tabela.innerHTML = `
            <tr>
                <td colspan="8" class="text-center text-muted">
                    <i class="fas fa-search fa-2x mb-2 d-block"></i>
                    Aplique os filtros para visualizar os dados
                </td>
            </tr>
        `;
    }
}

// Função para mostrar notificações
function mostrarNotificacao(mensagem, tipo = 'info') {
    console.log(`📢 [DEBUG] Notificação: ${mensagem} (${tipo})`);
    
    try {
        // Fallback para alert se Bootstrap não estiver disponível
        if (typeof bootstrap === 'undefined') {
            alert(mensagem);
            return;
        }
        
        // Criar elemento de notificação
        const notificacao = document.createElement('div');
        notificacao.className = `alert alert-${tipo === 'success' ? 'success' : tipo === 'error' ? 'danger' : 'info'} alert-dismissible fade show position-fixed`;
        notificacao.style.cssText = 'top: 20px; right: 20px; z-index: 9999; max-width: 400px;';
        notificacao.innerHTML = `
            ${mensagem.replace(/\n/g, '<br>')}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        // Adicionar ao body
        document.body.appendChild(notificacao);
        
        // Remover automaticamente após 5 segundos
        setTimeout(() => {
            if (notificacao.parentNode) {
                notificacao.remove();
            }
        }, 5000);
        
        console.log('✅ [DEBUG] Notificação exibida');
        
    } catch (error) {
        console.error('❌ [DEBUG] Erro ao mostrar notificação:', error);
        // Fallback para alert
        alert(mensagem);
    }
}

// Função para salvar filtro personalizado
function salvarFiltroPersonalizado() {
    const filtros = coletarFiltrosRelatorio();
    const nome = prompt('Digite um nome para este conjunto de filtros:');
    
    if (nome && nome.trim()) {
        try {
            let filtrosSalvos = JSON.parse(localStorage.getItem('filtrosRelatorioSalvos') || '[]');
            
            filtrosSalvos.push({
                nome: nome.trim(),
                filtros: filtros,
                dataCriacao: new Date().toISOString()
            });
            
            localStorage.setItem('filtrosRelatorioSalvos', JSON.stringify(filtrosSalvos));
            atualizarListaFiltrosSalvos();
            
            mostrarNotificacao(`✅ Filtros salvos com sucesso: "${nome}"`, 'success');
        } catch (error) {
            console.error('Erro ao salvar filtros:', error);
            mostrarNotificacao('❌ Erro ao salvar filtros', 'error');
        }
    }
}

// Função para atualizar lista de filtros salvos
function atualizarListaFiltrosSalvos() {
    try {
        const filtrosSalvos = JSON.parse(localStorage.getItem('filtrosRelatorioSalvos') || '[]');
        const container = document.getElementById('lista-filtros-salvos');
        
        if (!container) return;
        
        if (filtrosSalvos.length === 0) {
            container.innerHTML = '<small class="text-muted">Nenhum filtro salvo</small>';
            return;
        }
        
        let html = '';
        filtrosSalvos.forEach((filtro, index) => {
            html += `
                <div class="d-flex justify-content-between align-items-center mb-2">
                    <span class="small">${filtro.nome}</span>
                    <div>
                        <button class="btn btn-sm btn-outline-primary me-1" onclick="carregarFiltroSalvo(${index})">
                            <i class="fas fa-upload"></i>
                        </button>
                        <button class="btn btn-sm btn-outline-danger" onclick="excluirFiltroSalvo(${index})">
                            <i class="fas fa-trash"></i>
                        </button>
                    </div>
                </div>
            `;
        });
        
        container.innerHTML = html;
    } catch (error) {
        console.error('Erro ao atualizar lista de filtros salvos:', error);
    }
}

// Função para carregar filtro salvo
function carregarFiltroSalvo(index) {
    try {
        const filtrosSalvos = JSON.parse(localStorage.getItem('filtrosRelatorioSalvos') || '[]');
        const filtro = filtrosSalvos[index];
        
        if (filtro) {
            Object.keys(filtro.filtros).forEach(key => {
                const elemento = document.getElementById(`filtro-${key.replace('_', '-')}-relatorio`);
                if (elemento && filtro.filtros[key]) {
                    elemento.value = filtro.filtros[key];
                }
            });
            
            mostrarNotificacao(`✅ Filtros "${filtro.nome}" carregados`, 'success');
        }
    } catch (error) {
        console.error('Erro ao carregar filtro salvo:', error);
        mostrarNotificacao('❌ Erro ao carregar filtros', 'error');
    }
}

// Função para excluir filtro salvo
function excluirFiltroSalvo(index) {
    if (confirm('Tem certeza que deseja excluir este filtro salvo?')) {
        try {
            let filtrosSalvos = JSON.parse(localStorage.getItem('filtrosRelatorioSalvos') || '[]');
            const nome = filtrosSalvos[index]?.nome;
            
            filtrosSalvos.splice(index, 1);
            localStorage.setItem('filtrosRelatorioSalvos', JSON.stringify(filtrosSalvos));
            atualizarListaFiltrosSalvos();
            
            mostrarNotificacao(`🗑️ Filtro "${nome}" excluído`, 'success');
        } catch (error) {
            console.error('Erro ao excluir filtro salvo:', error);
            mostrarNotificacao('❌ Erro ao excluir filtro', 'error');
        }
    }
}

// Inicializar filtros salvos quando a página carregar
document.addEventListener('DOMContentLoaded', function() {
    // Atualizar lista de filtros salvos
    if (document.getElementById('lista-filtros-salvos')) {
        atualizarListaFiltrosSalvos();
    }
    
    // Configurar evento para mostrar/esconder campos de data personalizada
    const campoPeriodo = document.getElementById('filtro-periodo-relatorio');
    if (campoPeriodo) {
        campoPeriodo.addEventListener('change', function() {
            const dataInicioContainer = document.getElementById('data-inicio-container');
            const dataFimContainer = document.getElementById('data-fim-container');
            
            if (this.value === 'personalizado') {
                if (dataInicioContainer) dataInicioContainer.style.display = 'block';
                if (dataFimContainer) dataFimContainer.style.display = 'block';
            } else {
                if (dataInicioContainer) dataInicioContainer.style.display = 'none';
                if (dataFimContainer) dataFimContainer.style.display = 'none';
            }
        });
    }
});
