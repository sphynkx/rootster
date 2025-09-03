window._pell_instances = {};

function init_pell_for_row(rowId, html) {
    var editModeDiv = document.querySelector('tr[data-row-id="'+rowId+'"] td[data-col="data"] .edit-mode');
    if (!editModeDiv) return;
    // Flush edit-mode before the new editor creation
    editModeDiv.innerHTML = '';
    var editorDiv = document.createElement('div');
    editorDiv.className = 'pell-editor';
    editorDiv.id = 'pell-editor-' + rowId;
    editModeDiv.appendChild(editorDiv);

    var pellInstance = pell.init({
        element: editorDiv,
        onChange: function(html_out) {
            // TODO: Add live preview here
        },
        defaultParagraphSeparator: 'br'
    });

    // Set initial value
    pellInstance.content.innerHTML = html || '';
    window._pell_instances[rowId] = pellInstance;
}

function destroy_pell_for_row(rowId) {
    var old = document.getElementById('pell-editor-' + rowId);
    if (old) old.remove();
    window._pell_instances[rowId] = undefined;
}

function get_pell_html(rowId) {
    if (window._pell_instances[rowId]) {
        return window._pell_instances[rowId].content.innerHTML;
    }
    return '';
}