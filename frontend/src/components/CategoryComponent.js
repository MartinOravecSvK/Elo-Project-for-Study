import React from 'react';
import './CategoryComponent.css';

function CategoryComponent({ setCategory }) {
    return (
        <div className='CategoryWrapper'>
            <h1>
                Which category best describes this type of event/experience:
            </h1>
            <div className='CategoryButtons'>
                <button onClick={() => setCategory('Health')}>Health</button>
                <button onClick={() => setCategory('Financial')}>Financial</button>
                <button onClick={() => setCategory('Relationship')}>Relationship</button>
                <button onClick={() => setCategory('Bereavement')}>Bereavement</button>
                <button onClick={() => setCategory('Work')}>Work</button>
                <button onClick={() => setCategory('Crime')}>Crime</button>
            </div>
        </div>
    );
}

export default CategoryComponent;