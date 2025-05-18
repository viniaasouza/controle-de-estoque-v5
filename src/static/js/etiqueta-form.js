// Função para validar e formatar datas antes do envio
function validateAndFormatDates() {
    const dataFabricacao = document.getElementById('dataFabricacao').value;
    const dataValidade = document.getElementById('dataValidade').value;
    
    // Formatar datas para o formato ISO (YYYY-MM-DD)
    const isoDataFabricacao = formatDateToISO(dataFabricacao);
    const isoDataValidade = formatDateToISO(dataValidade);
    
    // Validar se as datas foram convertidas corretamente (devem estar no formato YYYY-MM-DD)
    const isoDatePattern = /^\d{4}-\d{2}-\d{2}$/;
    
    if (!isoDatePattern.test(isoDataFabricacao)) {
        alert('Formato de data de fabricação inválido. Use o formato DD/MM/YYYY.');
        return false;
    }
    
    if (!isoDatePattern.test(isoDataValidade)) {
        alert('Formato de data de validade inválido. Use o formato DD/MM/YYYY.');
        return false;
    }
    
    // Atualizar os valores dos campos com as datas formatadas
    document.getElementById('dataFabricacao').value = isoDataFabricacao;
    document.getElementById('dataValidade').value = isoDataValidade;
    
    return true;
}

// Função para formatar data para YYYY-MM-DD
function formatDateToISO(dateString) {
    if (!dateString) return '';
    
    // Se já estiver no formato YYYY-MM-DD, retorna como está
    if (/^\d{4}-\d{2}-\d{2}$/.test(dateString)) {
        return dateString;
    }
    
    // Tenta converter de DD/MM/YYYY para YYYY-MM-DD
    if (dateString.includes('/')) {
        const parts = dateString.split('/');
        if (parts.length === 3) {
            // Verifica se o ano tem 4 dígitos, se não, tenta deduzir (ex: 25 -> 2025)
            let year = parts[2];
            if (year.length === 2) {
                year = (parseInt(year, 10) < 70 ? '20' : '19') + year; // Heurística simples para anos de 2 dígitos
            }
            
            // Assume DD/MM/YYYY
            if (parts[0].length <= 2 && parts[1].length <= 2 && year.length === 4) {
                return `${year}-${parts[1].padStart(2, '0')}-${parts[0].padStart(2, '0')}`;
            }
        }
    }
    
    // Tenta converter de MM/DD/YYYY para YYYY-MM-DD (formato americano)
    if (dateString.includes('/')) {
        const parts = dateString.split('/');
        if (parts.length === 3) {
            let year = parts[2];
            if (year.length === 2) {
                year = (parseInt(year, 10) < 70 ? '20' : '19') + year;
            }
            
            // Assume MM/DD/YYYY
            if (parts[0].length <= 2 && parts[1].length <= 2 && year.length === 4) {
                // Verifica se o mês é válido (1-12)
                const month = parseInt(parts[0], 10);
                if (month >= 1 && month <= 12) {
                    return `${year}-${parts[0].padStart(2, '0')}-${parts[1].padStart(2, '0')}`;
                }
            }
        }
    }
    
    // Tenta converter de DD-MM-YYYY para YYYY-MM-DD
    if (dateString.includes('-')) {
        const parts = dateString.split('-');
        if (parts.length === 3) {
            // Se o primeiro segmento tem 4 dígitos, já pode estar no formato YYYY-MM-DD
            if (parts[0].length === 4) {
                // Verifica se é um ano válido
                const year = parseInt(parts[0], 10);
                if (year >= 1900 && year <= 2100) {
                    // Já está no formato YYYY-MM-DD
                    return dateString;
                }
            }
            
            let year = parts[2];
            if (year.length === 2) {
                year = (parseInt(year, 10) < 70 ? '20' : '19') + year;
            }
            
            // Assume DD-MM-YYYY
            if (parts[0].length <= 2 && parts[1].length <= 2 && year.length === 4) {
                return `${year}-${parts[1].padStart(2, '0')}-${parts[0].padStart(2, '0')}`;
            }
        }
    }
    
    // Tenta extrair data de formato textual (ex: "17 de maio de 2025")
    try {
        const date = new Date(dateString);
        if (!isNaN(date.getTime())) {
            return date.toISOString().split('T')[0];
        }
    } catch (e) {
        console.error("Erro ao converter data:", e);
    }
    
    // Se não conseguir converter, retorna como está
    return dateString;
}
