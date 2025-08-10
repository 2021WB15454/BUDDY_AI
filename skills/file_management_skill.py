"""
File & Document Management Module for BUDDY AI Assistant
Handles file organization, search, document tracking, and workspace management
"""

import asyncio
import logging
import json
import os
import shutil
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass, asdict
import uuid
import mimetypes
from pathlib import Path
import hashlib


@dataclass
class DocumentInfo:
    """Document metadata structure"""
    id: str
    file_path: str
    original_name: str
    file_type: str
    file_size: int
    mime_type: str
    tags: List[str]
    category: str
    description: str
    importance: str  # high, medium, low
    created_at: str
    modified_at: str
    last_accessed: str
    checksum: str
    project: str
    location: str  # physical location for physical documents
    
    def __post_init__(self):
        if not self.created_at:
            self.created_at = datetime.now().isoformat()
        if not self.modified_at:
            self.modified_at = self.created_at


@dataclass
class FileOperation:
    """File operation log entry"""
    id: str
    operation_type: str  # create, move, copy, delete, rename, backup
    source_path: str
    destination_path: str
    timestamp: str
    status: str  # success, failed, pending
    notes: str
    
    def __post_init__(self):
        if not self.timestamp:
            self.timestamp = datetime.now().isoformat()


class FileManager:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.documents_file = "learning_data/documents.json"
        self.operations_file = "learning_data/file_operations.json"
        self.documents = self._load_documents()
        self.operations = self._load_operations()
        self.logger.info("FileManager initialized.")
    
    def _load_documents(self) -> List[DocumentInfo]:
        """Load document metadata from file"""
        try:
            with open(self.documents_file, 'r', encoding='utf-8') as f:
                docs_data = json.load(f)
                return [DocumentInfo(**doc) for doc in docs_data]
        except (FileNotFoundError, json.JSONDecodeError):
            return []
    
    def _load_operations(self) -> List[FileOperation]:
        """Load file operations from file"""
        try:
            with open(self.operations_file, 'r', encoding='utf-8') as f:
                ops_data = json.load(f)
                return [FileOperation(**op) for op in ops_data]
        except (FileNotFoundError, json.JSONDecodeError):
            return []
    
    def _save_documents(self):
        """Save document metadata to file"""
        try:
            os.makedirs(os.path.dirname(self.documents_file), exist_ok=True)
            with open(self.documents_file, 'w', encoding='utf-8') as f:
                docs_data = [asdict(doc) for doc in self.documents]
                json.dump(docs_data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            self.logger.error(f"Error saving documents: {e}")
    
    def _save_operations(self):
        """Save file operations to file"""
        try:
            os.makedirs(os.path.dirname(self.operations_file), exist_ok=True)
            with open(self.operations_file, 'w', encoding='utf-8') as f:
                ops_data = [asdict(op) for op in self.operations]
                json.dump(ops_data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            self.logger.error(f"Error saving operations: {e}")
    
    def _calculate_checksum(self, file_path: str) -> str:
        """Calculate MD5 checksum of file"""
        try:
            hash_md5 = hashlib.md5()
            with open(file_path, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_md5.update(chunk)
            return hash_md5.hexdigest()
        except Exception:
            return ""
    
    def _get_file_info(self, file_path: str) -> Tuple[str, int, str]:
        """Get basic file information"""
        try:
            stat = os.stat(file_path)
            file_size = stat.st_size
            mime_type, _ = mimetypes.guess_type(file_path)
            if not mime_type:
                mime_type = "application/octet-stream"
            
            file_type = Path(file_path).suffix.lower()
            return file_type, file_size, mime_type
        except Exception:
            return "", 0, "unknown"
    
    async def register_document(self, file_path: str, tags: List[str] = None,
                              category: str = "", description: str = "",
                              importance: str = "medium", project: str = "",
                              location: str = "") -> str:
        """Register a document in the management system"""
        
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        # Check if already registered
        for doc in self.documents:
            if doc.file_path == file_path:
                raise ValueError(f"Document already registered: {file_path}")
        
        file_type, file_size, mime_type = self._get_file_info(file_path)
        checksum = self._calculate_checksum(file_path)
        
        document = DocumentInfo(
            id=str(uuid.uuid4())[:8],
            file_path=file_path,
            original_name=os.path.basename(file_path),
            file_type=file_type,
            file_size=file_size,
            mime_type=mime_type,
            tags=tags or [],
            category=category,
            description=description,
            importance=importance.lower(),
            created_at=datetime.now().isoformat(),
            modified_at=datetime.fromtimestamp(os.path.getmtime(file_path)).isoformat(),
            last_accessed=datetime.now().isoformat(),
            checksum=checksum,
            project=project,
            location=location
        )
        
        self.documents.append(document)
        self._save_documents()
        
        self.logger.info(f"Document registered: {file_path}")
        return document.id
    
    async def search_documents(self, query: str) -> List[DocumentInfo]:
        """Search documents by name, tags, description, etc."""
        if not query:
            return []
        
        query = query.lower()
        results = []
        
        for doc in self.documents:
            if (query in doc.original_name.lower() or
                query in doc.description.lower() or
                query in doc.category.lower() or
                query in doc.project.lower() or
                any(query in tag.lower() for tag in doc.tags) or
                query in doc.file_type.lower()):
                results.append(doc)
        
        # Sort by relevance and last accessed
        results.sort(key=lambda d: (
            0 if query in d.original_name.lower() else
            1 if query in d.description.lower() else 2,
            d.last_accessed
        ), reverse=True)
        
        return results
    
    async def get_documents_by_category(self, category: str) -> List[DocumentInfo]:
        """Get all documents in a specific category"""
        return [d for d in self.documents if d.category.lower() == category.lower()]
    
    async def get_documents_by_project(self, project: str) -> List[DocumentInfo]:
        """Get all documents for a specific project"""
        return [d for d in self.documents if d.project.lower() == project.lower()]
    
    async def get_documents_by_tag(self, tag: str) -> List[DocumentInfo]:
        """Get all documents with a specific tag"""
        return [d for d in self.documents if tag.lower() in [t.lower() for t in d.tags]]
    
    async def organize_files(self, source_dir: str, target_dir: str, 
                           organize_by: str = "type") -> Dict[str, Any]:
        """Organize files from source to target directory"""
        
        if not os.path.exists(source_dir):
            raise FileNotFoundError(f"Source directory not found: {source_dir}")
        
        os.makedirs(target_dir, exist_ok=True)
        
        organized_count = 0
        failed_count = 0
        operations = []
        
        for root, dirs, files in os.walk(source_dir):
            for file in files:
                source_path = os.path.join(root, file)
                
                try:
                    # Determine target subdirectory
                    if organize_by == "type":
                        file_ext = Path(file).suffix.lower()
                        if file_ext in ['.pdf', '.doc', '.docx', '.txt']:
                            subdir = "Documents"
                        elif file_ext in ['.jpg', '.jpeg', '.png', '.gif', '.bmp']:
                            subdir = "Images"
                        elif file_ext in ['.mp4', '.avi', '.mkv', '.mov']:
                            subdir = "Videos"
                        elif file_ext in ['.mp3', '.wav', '.flac']:
                            subdir = "Audio"
                        elif file_ext in ['.zip', '.rar', '.7z']:
                            subdir = "Archives"
                        else:
                            subdir = "Other"
                    elif organize_by == "date":
                        mod_time = datetime.fromtimestamp(os.path.getmtime(source_path))
                        subdir = mod_time.strftime("%Y-%m")
                    else:
                        subdir = "Organized"
                    
                    target_subdir = os.path.join(target_dir, subdir)
                    os.makedirs(target_subdir, exist_ok=True)
                    
                    target_path = os.path.join(target_subdir, file)
                    
                    # Handle filename conflicts
                    counter = 1
                    base_name, ext = os.path.splitext(file)
                    while os.path.exists(target_path):
                        new_name = f"{base_name}_{counter}{ext}"
                        target_path = os.path.join(target_subdir, new_name)
                        counter += 1
                    
                    # Move file
                    shutil.move(source_path, target_path)
                    
                    # Log operation
                    operation = FileOperation(
                        id=str(uuid.uuid4())[:8],
                        operation_type="move",
                        source_path=source_path,
                        destination_path=target_path,
                        timestamp=datetime.now().isoformat(),
                        status="success",
                        notes=f"Organized by {organize_by}"
                    )
                    operations.append(operation)
                    organized_count += 1
                    
                except Exception as e:
                    failed_count += 1
                    operation = FileOperation(
                        id=str(uuid.uuid4())[:8],
                        operation_type="move",
                        source_path=source_path,
                        destination_path="",
                        timestamp=datetime.now().isoformat(),
                        status="failed",
                        notes=f"Error: {str(e)}"
                    )
                    operations.append(operation)
        
        # Save operations
        self.operations.extend(operations)
        self._save_operations()
        
        return {
            "organized_count": organized_count,
            "failed_count": failed_count,
            "operations": len(operations)
        }
    
    async def backup_documents(self, backup_dir: str, 
                             categories: List[str] = None) -> Dict[str, Any]:
        """Backup documents to specified directory"""
        
        os.makedirs(backup_dir, exist_ok=True)
        
        backed_up = 0
        failed = 0
        total_size = 0
        
        for doc in self.documents:
            # Filter by categories if specified
            if categories and doc.category not in categories:
                continue
            
            if not os.path.exists(doc.file_path):
                failed += 1
                continue
            
            try:
                # Create backup path maintaining directory structure
                rel_path = os.path.relpath(doc.file_path)
                backup_path = os.path.join(backup_dir, rel_path)
                
                os.makedirs(os.path.dirname(backup_path), exist_ok=True)
                shutil.copy2(doc.file_path, backup_path)
                
                backed_up += 1
                total_size += doc.file_size
                
                # Log operation
                operation = FileOperation(
                    id=str(uuid.uuid4())[:8],
                    operation_type="backup",
                    source_path=doc.file_path,
                    destination_path=backup_path,
                    timestamp=datetime.now().isoformat(),
                    status="success",
                    notes="Document backup"
                )
                self.operations.append(operation)
                
            except Exception as e:
                failed += 1
                self.logger.error(f"Backup failed for {doc.file_path}: {e}")
        
        self._save_operations()
        
        return {
            "backed_up": backed_up,
            "failed": failed,
            "total_size_mb": round(total_size / (1024 * 1024), 2)
        }
    
    async def find_duplicates(self) -> Dict[str, List[DocumentInfo]]:
        """Find duplicate documents based on checksum"""
        checksum_map = {}
        
        for doc in self.documents:
            if doc.checksum:
                if doc.checksum not in checksum_map:
                    checksum_map[doc.checksum] = []
                checksum_map[doc.checksum].append(doc)
        
        # Return only groups with duplicates
        duplicates = {k: v for k, v in checksum_map.items() if len(v) > 1}
        return duplicates
    
    def get_storage_stats(self) -> Dict[str, Any]:
        """Get storage and document statistics"""
        total_docs = len(self.documents)
        total_size = sum(doc.file_size for doc in self.documents)
        
        # Category breakdown
        categories = {}
        for doc in self.documents:
            categories[doc.category] = categories.get(doc.category, 0) + 1
        
        # File type breakdown
        file_types = {}
        for doc in self.documents:
            file_types[doc.file_type] = file_types.get(doc.file_type, 0) + 1
        
        # Recent activity
        now = datetime.now()
        recent_docs = len([d for d in self.documents 
                          if (now - datetime.fromisoformat(d.created_at)).days <= 7])
        
        return {
            "total_documents": total_docs,
            "total_size_mb": round(total_size / (1024 * 1024), 2),
            "categories": categories,
            "file_types": file_types,
            "recent_documents": recent_docs,
            "total_operations": len(self.operations)
        }


class FileManagementSkill:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.file_manager = FileManager()
        self.logger.info("FileManagementSkill initialized.")
    
    async def handle_file_query(self, user_input: str, context: Dict[str, Any]) -> str:
        """Handle file and document management queries"""
        try:
            query_lower = user_input.lower().strip()
            
            # Register/track document
            if any(keyword in query_lower for keyword in ["register document", "track file", "add document"]):
                return await self._handle_register_document(user_input, context)
            
            # Search documents
            elif any(keyword in query_lower for keyword in ["find document", "search file", "locate document"]):
                return await self._handle_search_documents(user_input, context)
            
            # Organize files
            elif any(keyword in query_lower for keyword in ["organize files", "sort files", "clean up files"]):
                return await self._handle_organize_files(user_input, context)
            
            # Backup documents
            elif any(keyword in query_lower for keyword in ["backup documents", "backup files"]):
                return await self._handle_backup_documents(user_input, context)
            
            # Find duplicates
            elif any(keyword in query_lower for keyword in ["find duplicates", "duplicate files"]):
                return await self._handle_find_duplicates()
            
            # Storage statistics
            elif any(keyword in query_lower for keyword in ["storage stats", "file stats", "document stats"]):
                return await self._handle_storage_stats()
            
            # List by category/project
            elif any(keyword in query_lower for keyword in ["documents by category", "files by project", "show category"]):
                return await self._handle_list_by_category(user_input, context)
            
            # Default help
            else:
                return await self._handle_file_help()
                
        except Exception as e:
            self.logger.error(f"Error handling file query: {e}")
            return "I'm having trouble with file management right now. Please try again!"
    
    async def _handle_register_document(self, user_input: str, context: Dict[str, Any]) -> str:
        """Handle registering a new document"""
        return ("📄 **Document Registration**\n\n"
               "Feature in development! This will allow you to:\n\n"
               "• Register files in the document management system\n"
               "• Add metadata, tags, and categories\n"
               "• Track document versions and changes\n"
               "• Set importance levels and projects\n\n"
               "Example usage:\n"
               "'Register document: C:\\Documents\\report.pdf, category: work, tags: important'")
    
    async def _handle_search_documents(self, user_input: str, context: Dict[str, Any]) -> str:
        """Handle searching for documents"""
        # Extract search query
        query = user_input.lower()
        for keyword in ["find document", "search file", "locate document"]:
            query = query.replace(keyword, "").strip()
        
        if not query:
            return ("🔍 **Search Documents**\n\n"
                   "Please specify what to search for. Examples:\n"
                   "• 'Find document: budget report'\n"
                   "• 'Search file: contract'\n"
                   "• 'Locate document: presentation'")
        
        results = await self.file_manager.search_documents(query)
        
        if not results:
            return f"🔍 **No documents found** for '{query}'\n\nTry a different search term or register more documents."
        
        response = f"🔍 **Document Search Results** for '{query}' ({len(results)} found)\n\n"
        
        for doc in results[:5]:
            response += f"📄 **{doc.original_name}**\n"
            response += f"   📁 Path: {doc.file_path}\n"
            response += f"   📂 Category: {doc.category or 'Uncategorized'}\n"
            response += f"   📊 Size: {self._format_file_size(doc.file_size)}\n"
            
            if doc.tags:
                response += f"   🏷️ Tags: {', '.join(doc.tags)}\n"
            if doc.project:
                response += f"   🚀 Project: {doc.project}\n"
            if doc.description:
                response += f"   📝 {doc.description[:50]}...\n"
            
            response += f"   🆔 ID: {doc.id}\n\n"
        
        if len(results) > 5:
            response += f"... and {len(results) - 5} more results.\n\n"
        
        response += "💡 Use document ID for specific operations or narrow your search."
        
        return response
    
    async def _handle_organize_files(self, user_input: str, context: Dict[str, Any]) -> str:
        """Handle file organization"""
        return ("📁 **File Organization**\n\n"
               "Feature coming soon! This will help you:\n\n"
               "• Automatically sort files by type, date, or project\n"
               "• Clean up cluttered directories\n"
               "• Create organized folder structures\n"
               "• Move files to appropriate locations\n\n"
               "Example usage:\n"
               "'Organize files in Downloads folder by type'\n"
               "'Sort documents by date created'")
    
    async def _handle_backup_documents(self, user_input: str, context: Dict[str, Any]) -> str:
        """Handle document backup"""
        return ("💾 **Document Backup**\n\n"
               "Feature in development! This will enable:\n\n"
               "• Automatic backup of important documents\n"
               "• Scheduled backup routines\n"
               "• Selective backup by category or project\n"
               "• Backup verification and integrity checks\n\n"
               "Example usage:\n"
               "'Backup all work documents to external drive'\n"
               "'Create backup of project files'")
    
    async def _handle_find_duplicates(self) -> str:
        """Handle finding duplicate files"""
        duplicates = await self.file_manager.find_duplicates()
        
        if not duplicates:
            return ("✅ **No Duplicates Found**\n\n"
                   "Great! No duplicate documents detected in your system.\n"
                   "Your file management is well organized!")
        
        response = f"🔍 **Duplicate Documents Found** ({len(duplicates)} groups)\n\n"
        
        total_wasted_space = 0
        
        for i, (checksum, docs) in enumerate(duplicates.items(), 1):
            if i > 5:  # Show only first 5 groups
                response += f"... and {len(duplicates) - 5} more duplicate groups\n"
                break
            
            response += f"**Group {i}:** {len(docs)} identical files\n"
            
            for doc in docs:
                response += f"• {doc.original_name} ({self._format_file_size(doc.file_size)})\n"
                response += f"  📁 {doc.file_path}\n"
            
            # Calculate wasted space (keep one, others are wasted)
            wasted = sum(doc.file_size for doc in docs[1:])
            total_wasted_space += wasted
            response += f"💾 Wasted space: {self._format_file_size(wasted)}\n\n"
        
        response += f"📊 **Summary:**\n"
        response += f"• Total duplicate groups: {len(duplicates)}\n"
        response += f"• Total wasted space: {self._format_file_size(total_wasted_space)}\n\n"
        response += "💡 Consider keeping only one copy of each file to save space."
        
        return response
    
    async def _handle_storage_stats(self) -> str:
        """Handle storage statistics request"""
        stats = self.file_manager.get_storage_stats()
        
        response = f"📊 **Storage & Document Statistics**\n\n"
        
        response += f"**📈 Overview:**\n"
        response += f"• Total documents: {stats['total_documents']}\n"
        response += f"• Total storage used: {stats['total_size_mb']} MB\n"
        response += f"• Recent documents (7 days): {stats['recent_documents']}\n"
        response += f"• File operations logged: {stats['total_operations']}\n\n"
        
        if stats['categories']:
            response += f"**📂 By Category:**\n"
            for category, count in sorted(stats['categories'].items()):
                response += f"• {category or 'Uncategorized'}: {count} documents\n"
            response += "\n"
        
        if stats['file_types']:
            response += f"**📄 By File Type:**\n"
            sorted_types = sorted(stats['file_types'].items(), key=lambda x: x[1], reverse=True)
            for file_type, count in sorted_types[:10]:
                response += f"• {file_type or 'No extension'}: {count} files\n"
            response += "\n"
        
        # Storage insights
        response += f"**💡 Storage Insights:**\n"
        avg_size = stats['total_size_mb'] / stats['total_documents'] if stats['total_documents'] > 0 else 0
        response += f"• Average file size: {avg_size:.2f} MB\n"
        
        if stats['total_size_mb'] > 1000:
            response += f"• You have a large document collection!\n"
        elif stats['total_size_mb'] < 100:
            response += f"• Your document collection is well managed\n"
        
        response += f"• Consider organizing files by category for better management\n"
        response += f"• Regular backups recommended for important documents"
        
        return response
    
    async def _handle_list_by_category(self, user_input: str, context: Dict[str, Any]) -> str:
        """Handle listing documents by category or project"""
        return ("📂 **Browse by Category/Project**\n\n"
               "Feature coming soon! This will show:\n\n"
               "• Documents organized by category\n"
               "• Project-based file listings\n"
               "• Tag-based document groups\n"
               "• Hierarchical folder views\n\n"
               "Example usage:\n"
               "'Show documents by category: work'\n"
               "'List files for project: budget-2024'")
    
    def _format_file_size(self, size_bytes: int) -> str:
        """Format file size in human-readable format"""
        if size_bytes < 1024:
            return f"{size_bytes} B"
        elif size_bytes < 1024 * 1024:
            return f"{size_bytes / 1024:.1f} KB"
        elif size_bytes < 1024 * 1024 * 1024:
            return f"{size_bytes / (1024 * 1024):.1f} MB"
        else:
            return f"{size_bytes / (1024 * 1024 * 1024):.1f} GB"
    
    async def _handle_file_help(self) -> str:
        """Provide file management help"""
        response = f"📁 **File & Document Management Help**\n\n"
        
        response += f"**📄 Document Management:**\n"
        response += f"• 'Register document: [path]' - Track files\n"
        response += f"• 'Find document: [query]' - Search files\n"
        response += f"• 'Document stats' - Storage overview\n\n"
        
        response += f"**🗂️ Organization:**\n"
        response += f"• 'Organize files in [folder]' - Auto-sort files\n"
        response += f"• 'Show category: [name]' - List by category\n"
        response += f"• 'Files by project: [name]' - Project files\n\n"
        
        response += f"**🔍 Analysis:**\n"
        response += f"• 'Find duplicates' - Locate duplicate files\n"
        response += f"• 'Storage stats' - Usage statistics\n"
        response += f"• 'Recent documents' - Recently added files\n\n"
        
        response += f"**💾 Backup & Maintenance:**\n"
        response += f"• 'Backup documents to [path]' - Create backups\n"
        response += f"• 'Backup category: [name]' - Selective backup\n\n"
        
        response += f"**💡 Pro Tips:**\n"
        response += f"• Use categories to organize documents logically\n"
        response += f"• Add tags for better searchability\n"
        response += f"• Regular backups prevent data loss\n"
        response += f"• Remove duplicates to save storage space\n"
        response += f"• Set up organized folder structures early"
        
        return response


# For testing purposes
if __name__ == "__main__":
    import asyncio
    
    async def test_file_skill():
        skill = FileManagementSkill()
        
        test_queries = [
            "find document: report",
            "storage stats",
            "find duplicates",
            "organize files",
            "backup documents"
        ]
        
        print("🧪 Testing File Management Skill")
        print("=" * 50)
        
        for query in test_queries:
            print(f"\nQuery: '{query}'")
            response = await skill.handle_file_query(query, {})
            print(f"Response: {response[:200]}...")
            print("-" * 40)
    
    asyncio.run(test_file_skill())
