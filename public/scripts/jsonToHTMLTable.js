export function jsonToHTMLTable(jsonData) {
    if (jsonData.length === 0) return '<i>Conjunto vazio.</i>';

    const keys = Object.keys(jsonData[0]);
    let output = '<table border="1" cellpadding="5" cellspacing="0">\n';

    // Cabeçalho da tabela
    output += '  <thead>\n    <tr>\n';
    keys.forEach(key => {
        output += `      <th>${key}</th>\n`;
    });
    output += '    </tr>\n  </thead>\n';

    // Corpo da tabela com os registros
    output += '  <tbody>\n';
    jsonData.forEach(item => {
        output += '    <tr>\n';
        keys.forEach(key => {
            output += `      <td>${item[key] ?? ''}</td>\n`; // Usamos ?? para valores undefined ou null
        });
        output += '    </tr>\n';
    });
    output += '  </tbody>\n';

    output += '</table>';
    return output;
}
