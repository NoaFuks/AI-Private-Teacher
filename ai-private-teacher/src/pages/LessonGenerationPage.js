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
            const response = await axios.post('http://localhost:8000/api/generate-lesson', { name: studentName });
            setLessonSegments(response.data.lesson_segments);
            setQuestions(response.data.questions);
            setIsLoading(false);
        } catch (error) {
            console.error('Error generating lesson:', error);
            setIsLoading(false);
        }
    };

    const handleAnswerSubmit = async (e) => {
        e.preventDefault();
        const currentQuestion = questions[currentQuestionIndex];
        try {
            const response = await axios.post('http://localhost:8000/api/validate-answer', {
                student_answer: studentAnswer,
                correct_answer: currentQuestion.correct_answer,
                explanation: currentQuestion.explanation
            });
            const feedbackResponse = response.data.feedback;
            setFeedback(feedbackResponse);
            speakText(feedbackResponse);

            setShowNextSegmentButton(true);  // Show the "Next" button to go to the next segment
        } catch (error) {
            console.error('Error validating answer:', error);
        }
    };

    const handleQuestionSubmit = async (e) => {
        e.preventDefault();
        try {
            const response = await axios.post('http://localhost:8000/api/handle-question', { question: studentQuestion });
            setAnswerToQuestion(response.data.answer);
            speakText(response.data.answer);
            setStudentQuestion('');  // Clear the input after submission
            setShowNextButton(true);  // Show the "Next" button after answering
        } catch (error) {
            console.error('Error handling question:', error);
        }
    };

    const handleNoQuestion = () => {
        // Stop any currently speaking text before moving to the next segment
        window.speechSynthesis.cancel();

        setAskForQuestions(false);
        setStudentQuestion('');  // Clear any previous question input
        setStudentAnswer('');  // Clear any previous answer
    };

    const handleNext = () => {
        // Stop any currently speaking text before moving to the next segment
        window.speechSynthesis.cancel();

        setShowNextButton(false);
        setAskForQuestions(false);  // Hide the question form and move to the teacher's question
        setStudentAnswer('');  // Clear answer to question

        if (currentQuestionIndex < questions.length - 1) {
            setCurrentQuestionIndex(currentQuestionIndex + 1);
        } else {
            setShowNextSegmentButton(true);  // Show the "Next" button to go to the next segment
        }
    };

    const handleNextSegment = () => {
        // Stop any currently speaking text before moving to the next segment
        window.speechSynthesis.cancel();

        setShowNextSegmentButton(false);
        setFeedback('');  // Clear feedback
        setStudentAnswer('');  // Clear answer to question

        if (currentSegmentIndex < lessonSegments.length - 1) {
            setCurrentSegmentIndex(currentSegmentIndex + 1);
            setCurrentQuestionIndex(currentSegmentIndex + 1);  // Reset question for new segment
            setAskForQuestions(true);  // Ask for questions after the next segment
        } else {
            setFeedback('Lesson completed!');
        }
    };

    const speakText = (text) => {
        if ('speechSynthesis' in window) {
            // Stop any currently speaking text before starting new text
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
                                    <button type="button" className="btn btn-secondary ml-2" onClick={handleNoQuestion}>
                                        No Question
                                    </button>
                                </form>
                                {answerToQuestion && <div className="answer mt-3">{answerToQuestion}</div>}
                            </div>
                        ) : (
                            <>
                                {questions.length > 0 && currentQuestionIndex < questions.length && (
                                    <div className="question-section mt-4">
                                        <h3>{questions[currentQuestionIndex].question}</h3>
                                        <form onSubmit={handleAnswerSubmit}>
                                            <div className="form-group mb-3">
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