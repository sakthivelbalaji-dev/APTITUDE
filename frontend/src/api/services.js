import api from './axios'

export const studentApi = {
  register: (data) => api.post('/student/register', data),
  login: (data) => api.post('/student/login', data),
}

export const testApi = {
  start: (studentId) => api.post('/test/start', { student_id: studentId }),
  saveAnswer: (data) => api.post('/test/save-answer', {
    student_id: data.studentId,
    question_id: data.questionId,
    selected_option: data.selectedOption,
  }),
  submit: (data) => api.post('/test/submit', {
    student_id: data.studentId,
    disqualified: data.disqualified || false,
    disqualification_reason: data.disqualificationReason || null,
  }),
}

export const resultApi = {
  getByRoll: (rollNumber) => api.get(`/result/${rollNumber}`),
  getHistory: (rollNumber) => api.get(`/result/${rollNumber}/history`),
}

export const adminApi = {
  login: (data) => api.post('/admin/login', data),
  getStats: () => api.get('/results/stats'),
  getResults: (params) => api.get('/results', { params }),
  exportCsv: () => api.get('/results/export', { responseType: 'blob' }),
  getStudents: (params) => api.get('/students', { params }),
  getStudentResult: (id) => api.get(`/students/${id}`),
  getQuestions: (params) => api.get('/questions', { params }),
  createQuestion: (data) => api.post('/questions', data),
  updateQuestion: (id, data) => api.put(`/questions/${id}`, data),
  deleteQuestion: (id) => api.delete(`/questions/${id}`),
  bulkImport: (questions) => api.post('/questions/bulk-import', questions),
}
