
// Cleanup Script
async function cleanupObsoleteTasks() {
    if (!confirm('Run cleanup? This will delete the obsolete "tasks" collection from Cloud Storage (keeping Workflow and Scores safe).')) return;

    try {
        const userId = localStorage.getItem('az104SyncUserId');
        if (!userId) return alert('No User I D found.');

        const { deleteDoc, doc } = window._firestoreOps;
        const db = window._firebaseDB;

        await deleteDoc(doc(db, 'users', userId, 'tasks', 'main'));
        alert('✅ Cleanup Complete! Obsolete "tasks" data removed from cloud.');
    } catch (e) {
        alert('Error: ' + e.message);
    }
}
window.cleanupObsoleteTasks = cleanupObsoleteTasks;

