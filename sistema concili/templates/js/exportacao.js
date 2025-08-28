// Função para mostrar alertas
function showAlert(message, type = 'success') {
    const alertContainer = document.getElementById('alert-container');
    const alert = document.createElement('div');
    alert.className = `alert alert-${type} alert-custom alert-dismissible fade show`;
    alert.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    alertContainer.appendChild(alert);
    
    setTimeout(() => {
        alert.remove();
    }, 5000);
}

// Função para carregar arquivos disponíveis para exportação
function carregarArquivosDisponiveis() {
    fetch('/api/listar_arquivos_exportacao')
        .then(response => {
            if (!response.ok) {
                throw new Error('Erro ao carregar arquivos');
            }
            return response.json();
        })
        .then(data => {
            // Preencher lista de extratos
            atualizarListaExtratos(data.extratos);
            
            // Preencher lista de lançamentos
            atualizarListaLancamentos(data.lancamentos);
            
            // Preencher informações de conciliações
            atualizarListaConciliacoes(data.conciliacoes);
        })
        .catch(error => {
            console.error('Erro ao carregar arquivos:', error);
            showAlert('Erro ao carregar a lista de arquivos disponíveis', 'danger');
        });
}

// Função para atualizar a lista de extratos
function atualizarListaExtratos(extratos) {
    const extratosLista = document.getElementById('lista-extratos');
    const extratosCount = document.getElementById('extratos-count');
    extratosLista.innerHTML = '';
    
    if (extratos && extratos.length > 0) {
        let totalExtratos = 0;
        extratos.forEach(extrato => {
            totalExtratos += extrato.total;
            extratosLista.innerHTML += `
                <a href="#" 
                   class="list-group-item list-group-item-action d-flex justify-content-between align-items-center" 
                   onclick="handleExport(event, '/api/exporta_extratos?arquivo=${encodeURIComponent(extrato.arquivo)}')">
                    <div>
                        <i class="fas fa-file-csv me-2"></i>
                        ${extrato.arquivo}
                    </div>
                    <span class="badge bg-primary rounded-pill">${extrato.total} registros</span>
                </a>`;
        });
        extratosLista.innerHTML += `
            <a href="#" 
               class="list-group-item list-group-item-action list-group-item-primary" 
               onclick="handleExport(event, '/api/exporta_extratos')">
                <i class="fas fa-download me-2"></i>
                Exportar Todos os Extratos
            </a>`;
        extratosCount.textContent = totalExtratos;
    } else {
        extratosLista.innerHTML = '<div class="list-group-item text-muted">Nenhum extrato disponível para exportação</div>';
        extratosCount.textContent = '0';
    }
}

// Função para atualizar a lista de lançamentos
function atualizarListaLancamentos(lancamentos) {
    const lancamentosLista = document.getElementById('lista-lancamentos');
    const lancamentosCount = document.getElementById('lancamentos-count');
    lancamentosLista.innerHTML = '';
    
    if (lancamentos && lancamentos.length > 0) {
        let totalLancamentos = 0;
        lancamentos.forEach(lancamento => {
            totalLancamentos += lancamento.total;
            lancamentosLista.innerHTML += `
                <a href="#" 
                   class="list-group-item list-group-item-action d-flex justify-content-between align-items-center" 
                   onclick="handleExport(event, '/api/exporta_lancamentos?arquivo=${encodeURIComponent(lancamento.arquivo)}')">
                    <div>
                        <i class="fas fa-file-csv me-2"></i>
                        ${lancamento.arquivo}
                    </div>
                    <span class="badge bg-primary rounded-pill">${lancamento.total} registros</span>
                </a>`;
        });
        lancamentosLista.innerHTML += `
            <a href="#" 
               class="list-group-item list-group-item-action list-group-item-primary" 
               onclick="handleExport(event, '/api/exporta_lancamentos')">
                <i class="fas fa-download me-2"></i>
                Exportar Todos os Lançamentos
            </a>`;
        lancamentosCount.textContent = totalLancamentos;
    } else {
        lancamentosLista.innerHTML = '<div class="list-group-item text-muted">Nenhum lançamento disponível para exportação</div>';
        lancamentosCount.textContent = '0';
    }
}

// Função para atualizar a lista de conciliações
function atualizarListaConciliacoes(conciliacoes) {
    const conciliacoesLista = document.getElementById('lista-conciliacoes');
    const conciliacoesCount = document.getElementById('conciliacoes-count');
    conciliacoesLista.innerHTML = '';
    
    if (conciliacoes && conciliacoes.total > 0) {
        conciliacoesLista.innerHTML = `
            <a href="#" 
               class="list-group-item list-group-item-action d-flex justify-content-between align-items-center" 
               onclick="handleExport(event, '/api/exporta_conciliacoes')">
                <div>
                    <i class="fas fa-file-csv me-2"></i>
                    Exportar Conciliações
                </div>
                <span class="badge bg-primary rounded-pill">${conciliacoes.total} registros</span>
            </a>`;
        conciliacoesCount.textContent = conciliacoes.total;
    } else {
        conciliacoesLista.innerHTML = '<div class="list-group-item text-muted">Nenhuma conciliação disponível para exportação</div>';
        conciliacoesCount.textContent = '0';
    }
}

// Função para lidar com a exportação
async function handleExport(event, url) {
    event.preventDefault();
    
    try {
        // Mostrar loading
        showAlert('Preparando arquivo para download...', 'info');
        
        // Fazer a requisição
        const response = await fetch(url);
        
        // Verificar se a resposta é um JSON (erro) ou um blob (arquivo)
        const contentType = response.headers.get('content-type');
        if (contentType && contentType.includes('application/json')) {
            const data = await response.json();
            throw new Error(data.message || data.error || 'Erro ao exportar arquivo');
        }
        
        if (!response.ok) {
            throw new Error('Erro ao exportar arquivo');
        }
        
        // Obter o blob do arquivo
        const blob = await response.blob();
        
        // Criar nome do arquivo baseado na URL
        const fileName = url.includes('extratos') ? 'extratos.csv' :
                        url.includes('lancamentos') ? 'lancamentos.csv' :
                        'conciliacoes.csv';
        
        // Criar link de download
        const link = document.createElement('a');
        link.href = window.URL.createObjectURL(blob);
        link.download = fileName;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        
        // Mostrar mensagem de sucesso
        showAlert('Arquivo exportado com sucesso!', 'success');
        
    } catch (error) {
        console.error('Erro na exportação:', error);
        showAlert(error.message || 'Erro ao exportar arquivo', 'danger');
    }
}

// Carregar dados ao abrir a aba de relatórios
document.addEventListener('DOMContentLoaded', function() {
    const relatoriosTab = document.querySelector('a[href="#relatorios"]');
    if (relatoriosTab) {
        relatoriosTab.addEventListener('click', carregarArquivosDisponiveis);
    }
    
    // Carregar dados iniciais se já estiver na aba de relatórios
    if (window.location.hash === '#relatorios') {
        carregarArquivosDisponiveis();
    }
    
    // Configurar rotação dos ícones nas seções colapsáveis
    const collapses = document.querySelectorAll('.collapse');
    collapses.forEach(collapse => {
        collapse.addEventListener('show.bs.collapse', function() {
            const header = document.querySelector(`[data-bs-target="#${this.id}"]`);
            const icon = header.querySelector('.section-icon');
            icon.style.transform = 'rotate(90deg)';
        });
        
        collapse.addEventListener('hide.bs.collapse', function() {
            const header = document.querySelector(`[data-bs-target="#${this.id}"]`);
            const icon = header.querySelector('.section-icon');
            icon.style.transform = 'rotate(0deg)';
        });
    });
});
