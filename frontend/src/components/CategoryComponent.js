import React, { useState } from 'react';
import './CategoryComponent.css';

function CategoryComponent({ setCategory }) {
    const [selectedCategory, setSelectedCategory] = useState(null);

    const handleCategoryClick = (category) => {
        setSelectedCategory(category);
        setCategory(category);
    };

    return (
        <div className='CategoryWrapper'>
            <h1 className='question'>
                Which category best describes this type of event/experience:
            </h1>
            <div className='CategoryButtons'>
                {['Health', 'Financial', 'Relationship', 'Bereavement', 'Work', 'Crime'].map((category) => (
                    <div
                        key={category}
                        className={`category-button ${selectedCategory === category ? 'selected' : ''}`}
                        onClick={() => handleCategoryClick(category)}
                    >
                        {category}
                    </div>
                ))}
            </div>
        </div>
    );
}

export default CategoryComponent;
