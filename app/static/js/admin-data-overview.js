/**
 * AdminDataOverview - Reusable data overview component for admin panel
 * Provides pagination, search, and CRUD operations
 */
class AdminDataOverview {
    constructor(config) {
        this.config = {
            apiEndpoint: config.apiEndpoint,
            entityName: config.entityName || 'item',
            entityNamePlural: config.entityNamePlural || 'items',
            perPage: config.perPage || 10,
            tableColumns: config.tableColumns || [],
            rowActions: config.rowActions || [],
            searchDebounceTime: config.searchDebounceTime || 500
        };
        
        this.currentPage = 1;
        this.currentSearch = '';
        this.searchTimeout = null;
        this.isLoading = false;
    }
    
    /**
     * Initialize the component
     */
    init() {
        this.bindEvents();
        this.loadData();
    }
    
    /**
     * Bind event listeners
     */
    bindEvents() {
        // Search input
        const searchInput = document.getElementById('searchInput');
        if (searchInput) {
            searchInput.addEventListener('input', (e) => {
                clearTimeout(this.searchTimeout);
                this.searchTimeout = setTimeout(() => {
                    this.handleSearch(e.target.value);
                }, this.config.searchDebounceTime);
            });
        }
    }
    
    /**
     * Handle search input
     */
    handleSearch(query) {
        this.currentSearch = query.trim();
        this.currentPage = 1;
        this.loadData();
    }
    
    /**
     * Load data from API
     */
    async loadData() {
        if (this.isLoading) return;
        
        this.isLoading = true;
        this.showLoading();
        
        try {
            const params = new URLSearchParams({
                page: this.currentPage,
                per_page: this.config.perPage
            });
            
            if (this.currentSearch) {
                params.append('search', this.currentSearch);
            }
            
            const response = await fetch(`${this.config.apiEndpoint}?${params}`);
            const result = await response.json();
            
            if (result.success) {
                this.renderData(result.data);
                this.updateInfoDisplay(result.data.pagination);
            } else {
                this.showError(result.message || 'Failed to load data');
            }
        } catch (error) {
            console.error('Error loading data:', error);
            this.showError('Network error occurred');
        } finally {
            this.isLoading = false;
            this.hideLoading();
        }
    }
    
    /**
     * Render data in table
     */
    renderData(data) {
        const tableBody = document.getElementById('dataTableBody');
        const dataTableContainer = document.getElementById('dataTableContainer');
        const noDataContainer = document.getElementById('noDataContainer');
        
        if (!data.items || data.items.length === 0) {
            dataTableContainer.style.display = 'none';
            noDataContainer.style.display = 'block';
            return;
        }
        
        noDataContainer.style.display = 'none';
        dataTableContainer.style.display = 'block';
        
        // Clear existing rows
        tableBody.innerHTML = '';
        
        // Render rows
        data.items.forEach(item => {
            const row = document.createElement('tr');
            
            // Render columns
            this.config.tableColumns.forEach(column => {
                const cell = document.createElement('td');
                let value = this.getNestedValue(item, column.key);
                
                if (column.render && typeof column.render === 'function') {
                    cell.innerHTML = column.render(value, item);
                } else {
                    cell.textContent = value !== null && value !== undefined ? value : '-';
                }
                
                row.appendChild(cell);
            });
            
            // Render actions column
            if (this.config.rowActions.length > 0) {
                const actionsCell = document.createElement('td');
                const actionsDiv = document.createElement('div');
                actionsDiv.className = 'btn-group btn-group-sm';
                
                this.config.rowActions.forEach(action => {
                    const button = document.createElement('button');
                    button.type = 'button';
                    button.className = `btn ${action.class}`;
                    button.title = action.label;
                    button.innerHTML = `<i class="${action.icon}"></i>`;
                    button.addEventListener('click', () => action.action(item));
                    actionsDiv.appendChild(button);
                });
                
                actionsCell.appendChild(actionsDiv);
                row.appendChild(actionsCell);
            }
            
            tableBody.appendChild(row);
        });
        
        // Render pagination
        this.renderPagination(data.pagination);
    }
    
    /**
     * Render pagination controls
     */
    renderPagination(pagination) {
        const container = document.getElementById('paginationContainer');
        if (!container) return;
        
        container.innerHTML = '';
        
        if (pagination.pages <= 1) return;
        
        // Previous button
        const prevItem = document.createElement('li');
        prevItem.className = `page-item ${!pagination.has_prev ? 'disabled' : ''}`;
        prevItem.innerHTML = `
            <a class="page-link" href="#" data-page="${pagination.prev_num || 1}">
                <i class="fas fa-chevron-left"></i>
            </a>
        `;
        container.appendChild(prevItem);
        
        // Page numbers
        const startPage = Math.max(1, pagination.page - 2);
        const endPage = Math.min(pagination.pages, pagination.page + 2);
        
        if (startPage > 1) {
            this.addPageItem(container, 1, pagination.page);
            if (startPage > 2) {
                const ellipsis = document.createElement('li');
                ellipsis.className = 'page-item disabled';
                ellipsis.innerHTML = '<span class="page-link">...</span>';
                container.appendChild(ellipsis);
            }
        }
        
        for (let i = startPage; i <= endPage; i++) {
            this.addPageItem(container, i, pagination.page);
        }
        
        if (endPage < pagination.pages) {
            if (endPage < pagination.pages - 1) {
                const ellipsis = document.createElement('li');
                ellipsis.className = 'page-item disabled';
                ellipsis.innerHTML = '<span class="page-link">...</span>';
                container.appendChild(ellipsis);
            }
            this.addPageItem(container, pagination.pages, pagination.page);
        }
        
        // Next button
        const nextItem = document.createElement('li');
        nextItem.className = `page-item ${!pagination.has_next ? 'disabled' : ''}`;
        nextItem.innerHTML = `
            <a class="page-link" href="#" data-page="${pagination.next_num || pagination.pages}">
                <i class="fas fa-chevron-right"></i>
            </a>
        `;
        container.appendChild(nextItem);
        
        // Bind page click events
        container.addEventListener('click', (e) => {
            e.preventDefault();
            if (e.target.closest('a[data-page]')) {
                const page = parseInt(e.target.closest('a[data-page]').dataset.page);
                this.goToPage(page);
            }
        });
    }
    
    /**
     * Add page item to pagination
     */
    addPageItem(container, page, currentPage) {
        const item = document.createElement('li');
        item.className = `page-item ${page === currentPage ? 'active' : ''}`;
        item.innerHTML = `<a class="page-link" href="#" data-page="${page}">${page}</a>`;
        container.appendChild(item);
    }
    
    /**
     * Navigate to specific page
     */
    goToPage(page) {
        this.currentPage = page;
        this.loadData();
    }
    
    /**
     * Update info display
     */
    updateInfoDisplay(pagination) {
        const infoElement = document.getElementById('totalItemsInfo');
        if (infoElement) {
            const startItem = ((pagination.page - 1) * pagination.per_page) + 1;
            const endItem = Math.min(pagination.page * pagination.per_page, pagination.total);
            infoElement.textContent = `${startItem}-${endItem} of ${pagination.total} ${this.config.entityNamePlural}`;
        }
    }
    
    /**
     * Show loading state
     */
    showLoading() {
        const spinner = document.getElementById('loadingSpinner');
        const tableContainer = document.getElementById('dataTableContainer');
        const noDataContainer = document.getElementById('noDataContainer');
        
        if (spinner) spinner.style.display = 'block';
        if (tableContainer) tableContainer.style.display = 'none';
        if (noDataContainer) noDataContainer.style.display = 'none';
    }
    
    /**
     * Hide loading state
     */
    hideLoading() {
        const spinner = document.getElementById('loadingSpinner');
        if (spinner) spinner.style.display = 'none';
    }
    
    /**
     * Show error message
     */
    showError(message) {
        // You can implement a toast/alert system here
        console.error('Data overview error:', message);
        alert(`Error: ${message}`);
    }
    
    /**
     * Get nested object value by key path
     */
    getNestedValue(obj, key) {
        return key.split('.').reduce((o, k) => (o && o[k] !== undefined) ? o[k] : null, obj);
    }
    
    /**
     * Refresh data
     */
    refresh() {
        this.loadData();
    }
    
    /**
     * Reset filters and reload
     */
    reset() {
        this.currentPage = 1;
        this.currentSearch = '';
        const searchInput = document.getElementById('searchInput');
        if (searchInput) searchInput.value = '';
        this.loadData();
    }
}
