import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Icon from '../components/Icon';
import ReturnButton from '../components/ReturnButton';
import './LessonGenerationPage.css';

const LessonGenerationPage = () => {
    const [studentName, setStudentName] = useState('');
    const [lessonSegments, setLessonSegments] = useState([]);
    const [questions, setQuestions] = useState([]);
    const [currentSegmentIndex, setCurrentSegmentIndex] = useState(0);
    const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
    const [studentAnswer, setStudentAnswer] = useState('');
    const [feedback, setFeedback] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const [askForQuestions, setAskForQuestions] = useState(true);
    const [studentQuestion, setStudentQuestion] = useState('');
    const [answerToQuestion, setAnswerToQuestion] = useState('');
    const [showNextButton, setShowNextButton] = useState(false);
    const [showNextSegmentButton, setShowNextSegmentButton] = useState(false);
    const [pdfFile, setPdfFile] = useState(null); // New state for the uploaded PDF
    const [isListening, setIsListening] = useState(false); // Manage speech recognition state

    useEffect(() => {
        if (lessonSegments.length > 0 && currentSegmentIndex < lessonSegments.length) {
            speakText(lessonSegments[currentSegmentIndex]);
            setAskForQuestions(true);
        }
    }, [lessonSegments, currentSegmentIndex]);

    const handleGenerateLesson = async (e) => {
        e.preventDefault();
        setIsLoading(true);

        try {
            const formData = new FormData();
            formData.append('name', studentName);
            if (pdfFile) {
                formData.append('file', pdfFile); // Append the PDF file to the form data
            }

            const response = await axios.post('http://localhost:8000/api/generate-lesson', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                },
            });

            setLessonSegments(response.data.lesson_segments);
            setQuestions(response.data.questions);
            setIsLoading(false);
        } catch (error) {
            console.error('Error generating lesson:', error);
            setIsLoading(false);
        }
    };

    const handlePdfUpload = (e) => {
        setPdfFile(e.target.files[0]);
    };

    const handleAnswerSubmit = async (e) => {
        e.preventDefault();
        const currentQuestion = questions[currentQuestionIndex];
        try {
            const response = await axios.post('http://localhost:8000/api/validate-answer', {
                student_answer: studentAnswer,
                correct_answer: currentQuestion.correct_answer,
                explanation: currentQuestion.explanation,
                segment_index: currentSegmentIndex,
                student_name: studentName,
                segment_content: lessonSegments[currentSegmentIndex],
                question: currentQuestion.question
            });
            const feedbackResponse = response.data.feedback;
            setFeedback(feedbackResponse);
            speakText(feedbackResponse);

            setShowNextSegmentButton(true);
        } catch (error) {
            console.error('Error validating answer:', error);
        }
    };

    const handleQuestionSubmit = async (e) => {
        e.preventDefault();
        if (studentQuestion.trim() === '') return;

        try {
            const response = await axios.post('http://localhost:8000/api/handle-question', { question: studentQuestion });
            const aiAnswer = response.data.answer;
            setAnswerToQuestion(aiAnswer);
            speakText(aiAnswer);

            await axios.post('http://localhost:8000/api/save-progress', {
                student_name: studentName,
                segment_index: currentSegmentIndex,
                segment_content: lessonSegments[currentSegmentIndex],
                student_question: studentQuestion,
                answer_to_question: aiAnswer,
                asked_question: true
            });

            setStudentQuestion('');
            setShowNextButton(true);
        } catch (error) {
            console.error('Error handling question:', error);
        }
    };

    const handleNoQuestion = () => {
        window.speechSynthesis.cancel();
        setAskForQuestions(false);
        setStudentQuestion('');
        setStudentAnswer('');
    };

    const handleNext = () => {
        window.speechSynthesis.cancel();
        setShowNextButton(false);
        setAskForQuestions(false);
        setStudentAnswer('');

        if (currentQuestionIndex < questions.length - 1) {
            setCurrentQuestionIndex(currentQuestionIndex + 1);
        } else {
            setShowNextSegmentButton(true);
        }
    };

    const handleNextSegment = async () => {
        window.speechSynthesis.cancel();
        setShowNextSegmentButton(false);
        setFeedback('');
        setStudentAnswer('');
        setStudentQuestion('');
        setAnswerToQuestion('');

        if (currentSegmentIndex < lessonSegments.length - 1) {
            const segmentSummary = `Summary of segment ${currentSegmentIndex + 1}: ${lessonSegments[currentSegmentIndex]}`;

            await axios.post('http://localhost:8000/api/save-progress', {
                student_name: studentName,
                segment_index: currentSegmentIndex,
                segment_content: lessonSegments[currentSegmentIndex],
                summary: segmentSummary,
                student_question: studentQuestion,
                answer_to_question: answerToQuestion,
                asked_question: studentQuestion !== ''
            });

            setCurrentSegmentIndex(currentSegmentIndex + 1);
            setCurrentQuestionIndex(0);
            setAskForQuestions(true);
        } else {
            setFeedback('Lesson completed!');
        }
    };

    // Function to handle voice input using the Web Speech API
    const handleVoiceInput = () => {
        const recognition = new window.webkitSpeechRecognition();
        recognition.lang = 'en-US';
        recognition.continuous = false;
        recognition.interimResults = false;

        recognition.onstart = () => {
            setIsListening(true);
        };

        recognition.onresult = (event) => {
            let transcript = event.results[0][0].transcript;
            if (transcript === "one" || transcript === "won"){
                transcript = 1;
            }
            else if (transcript === "two" || transcript === "to" || transcript === "too"){
                transcript = 2;
            }
            else if (transcript === "three" || transcript === "tree"){
                transcript = 3;
            }
            else if (transcript === "four" || transcript === "for"){
                transcript = 4;
            }
            setStudentAnswer(transcript);  // Set the answer to the recognized speech
            setStudentQuestion(transcript);
        };

        recognition.onerror = (event) => {
            console.error('Error recognizing speech:', event.error);
        };

        recognition.onend = () => {
            setIsListening(false);  // Stop listening once the input is captured
        };

        recognition.start();
    };

    const speakText = (text) => {
        if ('speechSynthesis' in window) {
            window.speechSynthesis.cancel();

            const speech = new SpeechSynthesisUtterance(text);
            speech.lang = 'en-US';
            window.speechSynthesis.speak(speech);
        } else {
            alert("Sorry, your browser doesn't support text-to-speech.");
        }
    };

    return (
        <div className="lesson-page">
            <div className="lesson-card">
                <Icon size={80} />
                <h1 className="text-center mb-4">Lesson Generation</h1>
                {!lessonSegments.length && (
                    <form onSubmit={handleGenerateLesson}>
                        <div className="form-group mb-3">
                            <label htmlFor="studentName">Student Name:</label>
                            <input
                                type="text"
                                id="studentName"
                                className="form-control"
                                value={studentName}
                                onChange={(e) => setStudentName(e.target.value)}
                                placeholder="Enter student's name"
                                required
                            />
                        </div>
                        <div className="form-group mb-3">
                            <label htmlFor="pdfFile">Upload PDF for Lesson:</label>
                            <input
                                type="file"
                                id="pdfFile"
                                className="form-control"
                                onChange={handlePdfUpload}
                                accept="application/pdf"
                                required
                            />
                        </div>
                        <div className="d-grid gap-2">
                            <button type="submit" className="btn btn-primary btn-lg" disabled={isLoading}>
                                {isLoading ? 'Generating Lesson...' : 'Generate Lesson'}
                            </button>
                        </div>
                    </form>
                )}

                {lessonSegments.length > 0 && (
                    <>
                        <div className="lesson-content mt-4">
                            <h2>Lesson Segment:</h2>
                            <pre>{lessonSegments[currentSegmentIndex]}</pre>
                        </div>
                        {askForQuestions ? (
                            <div className="question-section mt-4">
                                <h3>Do you have any questions?</h3>
                                <form onSubmit={handleQuestionSubmit}>
                                    <div>
                                        <button type="button" className="btn btn-primary" onClick={handleVoiceInput}>
                                            {isListening ? 'Listening...' : 'Record question'}
                                        </button>
                                    </div>
                                    <div className="form-group mb-3">
                                        <input
                                            type="text"
                                            className="form-control"
                                            value={studentQuestion}
                                            onChange={(e) => setStudentQuestion(e.target.value)}
                                            placeholder="Enter your question"
                                        />
                                    </div>
                                    <button type="submit" className="btn btn-primary">Ask Question</button>
                                    <button type="button" className="btn btn-secondary" onClick={handleNoQuestion}>
                                        No Question
                                    </button>
                                </form>
                                {answerToQuestion && <div className="answer">{answerToQuestion}</div>}
                            </div>
                        ) : (
                            <>
                                {questions.length > 0 && currentQuestionIndex < questions.length && (
                                    <div className="question-section mt-4">
                                        <h3>{questions[currentQuestionIndex].question}</h3>
                                        <form onSubmit={handleAnswerSubmit}>
                                            <div>
                                                <button type="button" className="btn btn-primary" onClick={handleVoiceInput}>
                                                    {isListening ? 'Listening...' : 'Record Answer'}
                                                </button>
                                            </div>
                                            <div className="form-group">
                                                <input
                                                    type="text"
                                                    className="form-control"
                                                    value={studentAnswer}
                                                    onChange={(e) => setStudentAnswer(e.target.value)}
                                                    placeholder="Enter your answer"
                                                    required
                                                />
                                            </div>
                                            <button type="submit" className="btn btn-primary">Submit Answer</button>
                                        </form>
                                    </div>
                                )}

                                {feedback && <div className="feedback mt-3">{feedback}</div>}
                            </>
                        )}

                        {showNextButton && (
                            <div className="next-section mt-4">
                                <button type="button" className="btn btn-success" onClick={handleNext}>Next</button>
                            </div>
                        )}

                        {showNextSegmentButton && (
                            <div className="next-section mt-4">
                                <button type="button" className="btn btn-success" onClick={handleNextSegment}>Next Segment</button>
                            </div>
                        )}
                    </>
                )}
                <ReturnButton />
            </div>
        </div>
    );
};

export default LessonGenerationPage;
